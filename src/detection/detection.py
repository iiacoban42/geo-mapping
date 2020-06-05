# folder structure needs to be as follows:
# in the same folder as this script add 2 folders: train and validation
# both have folders: building, land, water
# in train put training images
# in validation put validation images
import os
import shutil
import time
import urllib

from keras.layers import Activation, Flatten, Dense, Dropout
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator

from core.models import Dataset as DatasetTable

os.chdir("detection")


#######################################    HELPER FUNCTIONS    ########################################################

def remove_images():
    directories = ['building', 'buildingland', 'buildinglandwater', 'buildingwater', 'land', 'landwater', 'water']
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)


def get_images():
    dataset = DatasetTable.objects.all()
    for row in dataset:
        x = str(row.x_coord)
        y = str(row.y_coord)
        year = str(row.year)
        res = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + year + \
              "/MapServer/tile/11/" + y + "/" + x
        label = ""
        if row.building == 1:
            label += 'building'
        if row.land == 1:
            label += 'land'
        if row.water == 1:
            label += 'water'
        if not os.path.exists(label):
            os.makedirs(label)
        urllib.request.urlretrieve(res, label + "/" + y + "_" + x + ".png")


remove_images()
print("done")


#################################           B E W A R E            ####################################################
#################################    CONVOLUTIAL NEURAL NETWORK    ####################################################

def CNN():
    IMG_SIZE = 256
    NB_CHANNELS = 3
    BATCH_SIZE = 2
    NB_TRAIN_IMG = 900
    NB_VALID_IMG = 1244
    cnn = Sequential()
    cnn.add(Conv2D(filters=32,
                   kernel_size=(8, 8),
                   strides=(2, 2),
                   padding='same',
                   input_shape=(IMG_SIZE, IMG_SIZE, NB_CHANNELS),
                   data_format='channels_last'))
    cnn.add(Activation('relu'))
    cnn.add(MaxPooling2D(pool_size=(2, 2),
                         strides=2))
    cnn.add(Conv2D(filters=64,
                   kernel_size=(4, 4),
                   strides=(1, 1),
                   padding='valid',
                   # input_shape=(IMG_SIZE,IMG_SIZE,NB_CHANNELS),
                   ))
    cnn.add(Activation('relu'))
    cnn.add(MaxPooling2D(pool_size=(2, 2),
                         strides=1))
    cnn.add(Conv2D(filters=64,
                   kernel_size=(2, 2),
                   strides=(1, 1),
                   padding='valid'))
    cnn.add(Activation('relu'))
    cnn.add(MaxPooling2D(pool_size=(2, 2),
                         strides=2))

    cnn.add(Conv2D(filters=64,
                   kernel_size=(2, 2),
                   strides=(1, 1),
                   padding='valid',
                   # input_shape=(IMG_SIZE,IMG_SIZE,NB_CHANNELS),
                   ))
    cnn.add(Activation('relu'))
    cnn.add(MaxPooling2D(pool_size=(2, 2),
                         strides=2))

    cnn.add(Flatten())
    cnn.add(Dense(64))
    cnn.add(Activation('relu'))
    cnn.add(Dropout(0.35))
    cnn.add(Dense(3))
    cnn.add(Activation('softmax'))
    cnn.load_weights('cnn_baseline.h5')
    cnn.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    train_datagen = ImageDataGenerator(
        horizontal_flip=True)
    validation_datagen = ImageDataGenerator(rescale=1. / 255)
    train_generator = train_datagen.flow_from_directory(
        'train',
        target_size=(IMG_SIZE, IMG_SIZE),
        class_mode='categorical',
        batch_size=BATCH_SIZE)
    validation_generator = validation_datagen.flow_from_directory(
        'validation',
        target_size=(IMG_SIZE, IMG_SIZE),
        class_mode='categorical',
        batch_size=BATCH_SIZE)

    start = time.time()
    cnn.fit_generator(
        train_generator,
        steps_per_epoch=NB_TRAIN_IMG // BATCH_SIZE,
        epochs=5,
        validation_data=validation_generator,
        validation_steps=NB_VALID_IMG // BATCH_SIZE)
    end = time.time()
    print('Processing time:', (end - start) / 60)

    # Save weights
    cnn.save_weights('cnn_baseline.h5')

    # Remove contents of the train and validation directories
    remove_images('train')
    remove_images('validation')
