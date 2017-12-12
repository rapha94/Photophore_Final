from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.models import model_from_json
import numpy

dogs = numpy.genfromtxt("assets/dogs.csv", delimiter=",", dtype="str")
cats = numpy.genfromtxt("assets/cats.csv", delimiter=",", dtype="str")

json_file = open('Scripts/VGG16/vgg16.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("Scripts/VGG16/vgg16.h5")


def getTags(path):
    image = load_img(path, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    yhat = model.predict(image)
    label = decode_predictions(yhat)
    result = []
    for item in label[0]:
        array = []
        for element in item:
            array.append(element)
        result.append(array)
    for item in result:
        if item[1] in dogs:
            item[1] = "dog"
        if item[1] in cats:
            item[1] = "cat"
        item[1] = item[1].replace('_', ' ')
    return result
