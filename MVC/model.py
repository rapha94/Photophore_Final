import os
import sqlite3
from Scripts import surf
from Models import data, tagData
from Scripts.VGG16 import vgg16


class Model:
    def __init__(self, controller):
        self.controller = controller

        self.elementList = []
        self.filterList = []
        self.tagList = []
        self.workingId = -1
        self.switched = False

        self.defaultElement = data.Data(-1, -1, os.getcwd() + "/assets/blank.png", [])

        self.load()

    def vgg16(self, path):
        print("run")
        for item in vgg16.getTags(path):
            if item[2] > 0.4:
                if item[1].upper() not in self.getElement(path).tags:
                    self.getElement(path).tags.append(item[1].upper())
                    if item[1] not in self.tagList:
                        self.newTag(item[1].upper())
        self.save()
        self.load()
        self.controller.view.update(self)
        print("done")

    def getElement(self, id):
        if isinstance(id, int):
            if self.workingId == -1:
                return self.defaultElement
            else:
                for element in self.elementList:
                    if element.id == id:
                        return element
        else:
            for element in self.elementList:
                if element.path == id:
                    return element

    def getDistanceList(self):
        list = []
        data = self.getElement(self.workingId)
        try:
            conn = sqlite3.connect(os.getcwd() + '/database.db')
            cursor = conn.cursor()
            cursor.execute(
                """SELECT data_id1,data_id2 FROM distances WHERE data_id1=? OR data_id2=? ORDER BY value DESC LIMIT 10""",
                (data.id, data.id))
            for row in cursor:
                if row[0] == data.id:
                    list.append(self.getElement(row[1]))
                else:
                    list.append(self.getElement(row[0]))
        except Exception as e:
            print("getDistances : " + str(e))
        finally:
            conn.close()
            return list

    def checkFile(self, path):
        try:
            conn = sqlite3.connect(os.getcwd() + '/database.db')
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM data WHERE path=?""", (path,))
            for row in cursor:
                conn.close()
                return True
            conn.close()
            return False
        except Exception as e:
            print("checkFile : " + str(e))

    def calculDistance(self, path):
        conn = sqlite3.connect(os.getcwd() + '/database.db')
        for element in self.elementList:
            if element.path != path:
                cursor2 = conn.cursor()
                cursor2.execute("""SELECT id FROM data WHERE path=?""", (path,))
                var = []
                for row in cursor2:
                    var.append(row)
                for row in var:
                    id = row[0]
                    try:
                        if id < element.id:
                            cursor = conn.cursor()
                            cursor.execute("""INSERT INTO distances(data_id1, data_id2, value) VALUES(?, ?, ?)""",
                                           (id, element.id, surf.distance(path, element.path)))
                        else:
                            cursor = conn.cursor()
                            cursor.execute("""INSERT INTO distances(data_id2, data_id1, value) VALUES(?, ?, ?)""",
                                           (id, element.id, surf.distance(path, element.path)))
                        conn.commit()
                    except Exception as e:
                        print("calculDistances : " + str(e))
                        conn.rollback()
        conn.close()

    def newData(self, path):
        try:
            conn = sqlite3.connect(os.getcwd() + '/database.db')
            cursor2 = conn.cursor()
            cursor2.execute("""SELECT MAX(rank) FROM data""")
            for row in cursor2:
                if row[0]:
                    max = row[0]
                else:
                    max = 0
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO data(rank, path) VALUES(?, ?)""", (max + 1, path))
            conn.commit()
        except Exception as e:
            print("newData : " + str(e))
            conn.rollback()
        finally:
            conn.close()

    def deleteData(self, id):
        try:
            conn = sqlite3.connect(os.getcwd() + '/database.db')
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM data WHERE id=?""", (id,))
            cursor.execute("""DELETE FROM tags WHERE data_id=?""", (id,))
            cursor.execute("""DELETE FROM distances WHERE data_id1=? OR data_id2=?""", (id, id))
            conn.commit()
        except Exception as e:
            print("deleteTag : " + str(e))
            conn.rollback()
        finally:
            conn.close()
            self.save()
            self.load()

    def newTag(self, text):
        try:
            conn = sqlite3.connect(os.getcwd() + '/database.db')
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO mainTags(bool, text) VALUES(?, ?)""", (0, text))
            conn.commit()
        except Exception as e:
            print("newTag : " + str(e))
            conn.rollback()
        finally:
            conn.close()
            self.save()
            self.load()

    def deleteTag(self, id):
        try:
            conn = sqlite3.connect(os.getcwd() + '/database.db')
            cursor = conn.cursor()
            cursor.execute("""SELECT text FROM mainTags WHERE id=?""", (id,))
            for row in cursor:
                text = str(row[0])
            for element in self.elementList:
                for tag in element.tags:
                    if tag == text:
                        element.tags.remove(tag)
            cursor.execute("""DELETE FROM mainTags WHERE id=?""", (id,))
            conn.commit()
        except Exception as e:
            print("deleteTag : " + str(e))
            conn.rollback()
        finally:
            conn.close()
            self.save()
            self.load()

    def checkData(self):
        try:
            conn = sqlite3.connect(os.getcwd() + '/database.db')
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM data""")
            for row in cursor:
                if not os.path.isfile(row[2]):
                    cursor2 = conn.cursor()
                    cursor2.execute("""DELETE FROM data WHERE id=?""", (str(row[0]),))
                    cursor2.execute("""DELETE FROM tags WHERE data_id=?""", (str(row[0]),))
                    cursor2.execute("""DELETE FROM distances WHERE data_id1=? OR data_id2=?""",
                                    (str(row[0]), str(row[0])))
            conn.commit()
        except Exception as e:
            print("checkData : " + str(e))
            conn.rollback()
        finally:
            conn.close()

    def load(self):
        del self.elementList[:]
        del self.tagList[:]
        del self.filterList[:]
        self.checkData()
        try:
            conn = sqlite3.connect(os.getcwd() + '/database.db')
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM data""")
            for row in cursor:
                cursor2 = conn.cursor()
                cursor2.execute("""SELECT text FROM tags WHERE data_id=?""", (str(row[0]),))
                tags = []
                for row2 in cursor2:
                    tags.append(row2[0])
                self.elementList.append(data.Data(row[0], row[1], row[2], tags))
            cursor.execute("""SELECT * FROM mainTags""")
            for row in cursor:
                if row[2]:
                    self.filterList.append(row[1])
                self.tagList.append(tagData.TagData(row[0], row[1], row[2]))
        except Exception as e:
            print("load : " + str(e))
        finally:
            conn.close()

    def save(self):
        try:
            conn = sqlite3.connect(os.getcwd() + '/database.db')
            cursor3 = conn.cursor()
            cursor3.execute("""DELETE FROM tags""")
            for element in self.elementList:
                cursor = conn.cursor()
                cursor.execute("""UPDATE data SET rank=? WHERE id=?""", (element.rank, element.id))
                for tag in element.tags:
                    cursor2 = conn.cursor()
                    cursor2.execute("""INSERT INTO tags(data_id, text) VALUES(?, ?)""", (element.id, tag))
            for element in self.tagList:
                cursor = conn.cursor()
                cursor.execute("""UPDATE mainTags SET bool=? WHERE id=?""", (element.check, element.id))
            conn.commit()
        except Exception as e:
            print("save : " + str(e))
            conn.rollback()
        finally:
            conn.close()
