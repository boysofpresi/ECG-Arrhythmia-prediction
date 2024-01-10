# -*- coding: utf-8 -*-
"""Copy of ecg Untitled23.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UhpIKea-tuwJWyIPqXBWjmbwtoDxBkUk
"""



#extract th e zip folder
!unzip "/content/ECG-Dataset" -d "/content/ECG-Dataset"

#import the nueral network libraries
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

#import the cnn layers
from tensorflow.keras.layers import Convolution2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten

"""##Image Preprocessing

"""

from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen=ImageDataGenerator(rescale=1./255,shear_range=0.2,zoom_range=0.2,horizontal_flip=True)

test_datagen=ImageDataGenerator(rescale=1./255)

x_train =train_datagen.flow_from_directory("/content/ECG-Dataset/Dataset/train",target_size=(64,64),batch_size=32,class_mode="categorical")

x_test = test_datagen.flow_from_directory("/content/ECG-Dataset/Dataset/test",target_size=(64,64),batch_size=32,class_mode="categorical")

x_train.class_indices

#initialize the model
model=Sequential()

#convolutional model
model.add(Convolution2D(32,(3,3),input_shape=(64,64,3),activation="relu"))
#here 32 indiates no.of feature detectors and(3,3) is feature detector size

#pooling layer
model.add(MaxPooling2D(pool_size=(2,2)))

#flatten layer
model.add(Flatten())

"""##Hidden layers"""

model.add(Dense(units=200,activation="relu",kernel_initializer="random_uniform"))

model.add(Dense(units=300,activation="relu",kernel_initializer="random_uniform"))

"""##Output layer"""

model.add(Dense(units=6,activation="softmax",kernel_initializer="random_uniform"))

"""##Compile model



"""

model.compile(optimizer="adam",loss="categorical_crossentropy",metrics=["accuracy"])

"""##train your model"""

tr=model.fit_generator(x_train,steps_per_epoch=480,epochs=25,validation_data=x_test,validation_steps=10)
#steps_per_epoch =>total trainging images/batch size
#validation_steps=>total testing images/batch size

tr.history

"""##To save the best accuracy got in the epoch we will use this callback and checkpoint"""

from tensorflow.keras.callbacks import ModelCheckpoint
checkpoint = ModelCheckpoint("best_model_{epoch:02d}.h5",monitor="val_accuracy",save_best_only=True,mode="Max")
tr = model.fit_generator(x_train,steps_per_epoch=480,callbacks=[checkpoint],validation_steps=10)

"""##saving the model"""

#for storing temporary
model.save('ECG.h5')

#for storing permanent in drive
model.save("/content/ECG.h5")

dict = tr.history
dict

losses=tr.history['loss']
accuracy=tr.history['accuracy']
epochs=list(range(1,26))

import matplotlib.pyplot as plt
plt.plot(range(1, 26), losses, label='Training Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

plt.scatter(epochs,accuracy)
plt.xlabel("epochs")
plt.ylabel("accuracy")
plt.show()

losses=tr.history['loss']
accuracy=tr.history['accuracy']
val_accuarcy=tr.history['val_accuracy']
epochs=list(range(1,26))

plt.plot(epochs,val_accuarcy)
plt.xlabel("epochs")
plt.ylabel("accuracy")
plt.show()

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the saved model
loaded_model = load_model('ECG.h5')
loaded_model.summary()

# Function to preprocess the input image
def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(64, 64))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Rescale to match the same scale used during training
    return img_array

# Replace 'path_to_your_image' with the actual path to the image you want to test
test_image_path = 'fig_25.png'
preprocessed_image = preprocess_image(test_image_path)

# Make predictions
predictions = loaded_model.predict(preprocessed_image)
predicted_class = np.argmax(predictions)

# Print the predicted class
print("Predicted Class:", predicted_class)

def interchange_key_value(dict1):
  dict2 = {}
  for key, value in dict1.items():
    dict2[value] = key
  return dict2

# Map class indices to class labels
class_indices = {'Left Bundle Branch Block': 0, 'Normal': 1, 'Premature Atrial Contraction': 2, 'Premature Ventricular Contractions': 3, 'Right Bundle Branch Block': 4, 'Ventricular Fibrillation': 5}
# print(class_indices)
# # reverse_class_indices = dict((v, k) for k, v in class_indices.items())
reverse_class_indices =interchange_key_value(class_indices)

predicted_class_label = reverse_class_indices[predicted_class]

# # Print the predicted class label
print("Predicted Class Label:", predicted_class_label)
