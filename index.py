import os
import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as plt_image
plt.style.use('seaborn')

import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image as keras_image

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D
from tensorflow.keras.layers import Flatten, Dense, Dropout

from tensorflow.keras.callbacks import TensorBoard
import cv2 as cv

from PIL import Image, ImageOps

def plot(hist):
  history = hist.history
  history['epoch'] = hist.epoch

  plt.figure(figsize=(12, 5))

  plt.subplot(121)
  plt.plot(history['epoch'], history['loss'], label='Loss')
  plt.plot(history['epoch'], history['val_loss'], label='Val Loss', color='orange')
  plt.legend()

  plt.subplot(122)
  plt.plot(history['epoch'], history['accuracy'], label='Acc')
  plt.plot(history['epoch'], history['val_accuracy'], label='Val Acc', color='orange')
  plt.legend()

  return plt.show()


# def test(model, width):
#   test_images_paths = os.listdir('datasetv4/prediction')  
#   for path in test_images_paths:
#     image_path = os.path.join('datasetv4/prediction', path)

#     image = keras_image.load_img(image_path,                                 
#                                  target_size=(width, width))
#     image = ImageOps.grayscale(image)
#     x = keras_image.img_to_array(image)
#     x = np.expand_dims(x, axis=0)

#     test_image = np.vstack([x])
#     result = model.predict(test_image, batch_size=8)

#     print(image_path)
#     print(classes[np.argmax(result)])

#     preview = plt_image.imread(image_path)
#     plt.imshow(image)
#     plt.show()
#   return print('Prediction Done')

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def testimg(model, width, img):  
  classes = ['ba', 'ca', 'da', 'dha', 'ga', 'ha', 'ja', 'ka', 'la', 'ma',
           'na', 'nga', 'nya', 'pa', 'ra', 'sa', 'ta', 'tha', 'wa', 'ya']
  # classes = ['ba', 'bu', 'ca', 'cu', 'da', 'du', 'e', 'e+' 'dha', 'dhu', 'ga', 'gu', 'ha', 'hu', 'i', 'ja', 'ju', 'ka', 'ku', 'la', 'lu', 'ma', 'mu',
  # 'na', 'nu', 'nga', 'ngu', 'nya', 'nyu', 'o', 'pa', 'pu', 'ra', 'ru', 'sa', 'su', 'ta', 'tu', 'tha', 'thu', 'wa', 'wu', 'ya', 'yu']
  # x = keras_image.img_to_array(img)
  # x = np.asarray(img)
  # apik img = cv.resize(img, (98, 98))
  img = cv.resize(img, (int(84 * img.shape[1] / img.shape[0]), 84))
  image = Image.fromarray(img.astype('uint8'), 'RGB')
  widthlocal, heightlocal = image.size
  widthsize = int(112 - (widthlocal / 2))
  heightsize = int(112 - (heightlocal / 2))

  image = add_margin(image, heightsize, widthsize, heightsize, widthsize, (255, 255, 255))
  image = image.resize((width, width))
  image = ImageOps.grayscale(image)  
  # x = np.expand_dims(x, axis=0)  
  x = keras_image.img_to_array(image)
  x = np.expand_dims(x, axis=0)

  test_image = np.vstack([x])
  result = model.predict(test_image, batch_size=8)

  # print(image_path)
  # print(classes[np.argmax(result)])

  # plt.imshow(image)
  # plt.show()
  return classes[np.argmax(result)]


def run(img):
  base_model = tf.keras.models.load_model('baselinemodel4/base_model.h5')

  base_model.compile(
      loss='categorical_crossentropy',
      optimizer='Adam',
      metrics=['accuracy']
  )

  # base_model.summary()

  # img = cv.imread('img/hanacaraka.png')

  scale = 50
  width = int(img.shape[1] * scale / 100)
  height = int(img.shape[0] * scale / 100)
  dim = (width, height)

  img = cv.resize(img, dim, interpolation=cv.INTER_AREA)
  imgbox = img.copy()

  gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
  thresh, bw = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)

  kernelerosion = np.ones((1, 1),np.uint8)
  imgerode = cv.erode(bw, kernelerosion)

  kerneldilation = np.ones((4, 4), np.uint8)
  imgdilation = cv.dilate(imgerode, kerneldilation)

  contours, _ = cv.findContours(imgdilation, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
  sorted_contours = sorted(contours, key=lambda ctr: cv.boundingRect(ctr)[0] + cv.boundingRect(ctr)[1] * imgdilation.shape[1] )

  rectd = []
  # tunningan
  minarea = 20
  maxarea = 2000

  # cv.drawContours(imgbox, contours, -1, (0, 0, 255), 3)
  imgshow = imgbox.copy()

  for cnt in sorted_contours:
      if(cv.contourArea(cnt) > minarea and cv.contourArea(cnt) < maxarea):
          box = cv.boundingRect(cnt)
          x, y, w, h = box
          rectd.append([x, y, w, h])                        
          cv.rectangle(imgshow, (x, y), (int(x + w), int(y + h)), (0, 0, 255), 1)

  finalword = ""
  for i in range(0, len(rectd)):
    final = imgbox[rectd[i][1]:rectd[i][1] + rectd[i][3], rectd[i][0]:rectd[i][0] + rectd[i][2]] 
    eachword = testimg(base_model, 224, final) 
    finalword += str(eachword) + " "
    # final = final[...,::-1]
    # final = final[...,::-1].astype(np.float32)
    # testimg(base_model, 224, final) 
  #   eachword = testimg(base_model, 224, final) 
  #   finalword += str(eachword) + " "

  return finalword
# plt.imshow(imgshow)
# plt.show()