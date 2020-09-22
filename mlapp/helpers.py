import tensorflow as tf
from django.conf import settings
import numpy as np
import cv2


def process_image(img):
    print(img)
    img_array = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (100, 100))
    input_img = np.array(new_array)
    input_img = input_img/255
    input_img = input_img.reshape(-1,100,100,1)
    return input_img


def predict(img_array):
    prediction_model = tf.keras.models.load_model(settings.MODEL_PATH)
    prediction = prediction_model.predict(img)
    result = np.argmax(prediction)
    return result

