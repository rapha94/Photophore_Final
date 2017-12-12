import sqlite3
import os

conn = sqlite3.connect(os.getcwd()+'/database.db')

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE data(
     id INTEGER PRIMARY KEY UNIQUE,
     rank INTEGER,
     path TEXT UNIQUE
)
""")
cursor.execute("""
CREATE TABLE tags(
     data_id INTEGER REFERENCES data(id),
     text TEXT
)
""")
cursor.execute("""
CREATE TABLE mainTags(
     id INTEGER PRIMARY KEY UNIQUE,
     text TEXT UNIQUE,
     bool INTEGER
)
""")
cursor.execute("""
CREATE TABLE distances(
     data_id1 INTEGER REFERENCES data(id),
     data_id2 INTEGER REFERENCES data(id),
     value DOUBLE,
     UNIQUE (data_id1, data_id2)
)
""")
conn.commit()

conn.close()
