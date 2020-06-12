# folder structure needs to be as follows:
# in the same folder as this script add 2 folders: train and validation
# both have folders: building, land, water
# in train put training images
# in validation put validation images
import os
import shutil
import time
import urllib

import numpy as np
from keras.layers import Activation, Flatten, Dense, Dropout
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator

from core.models import Dataset as DatasetTable

os.chdir('detection')

# choose which labels to use
labels = ['building', 'buildingland', 'buildinglandwater', 'buildingwater', 'land', 'landwater', 'water']
splits = ['train', 'validation']


#######################################    HELPER FUNCTIONS    ########################################################


# removes directory and subdirectories of directory
def remove_images(directory):
    for directory in directory:
        if os.path.exists(directory):
            shutil.rmtree(directory)


# saves images from the db in folders based on their label
# see @labels
def get_images():
    print('This will take a while..')
    dataset = DatasetTable.objects.all()
    for row in dataset:
        x = str(row.x_coord)
        y = str(row.y_coord)
        year = str(row.year)
        res = 'https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_' + year + \
              '/MapServer/tile/11/' + y + '/' + x
        label = ''
        if row.building == 1:
            label += 'building'
        if row.land == 1:
            label += 'land'
        if row.water == 1:
            label += 'water'
        if labels.__contains__(label):
            if not os.path.exists(label):
                os.makedirs(label)
            try:
                urllib.request.urlretrieve(res, label + '/' + y + '_' + x + '.png')
            except:
                'not found'
                print('Tile from', year, 'having x=', x, 'and y=', y, 'is not on the website. Delete it.\n')
    print('\ndatabase hacked\n')


# split the images in two sets: train and validation
# result: train/building, train/water, train/buildingwater... (same for validation)
def train_validation_split():
    NB_TRAIN_IMG = 0
    NB_VALID_IMG = 0
    train_ratio = 0.8
    print('Using', train_ratio, 'of the images for training and', round(1 - train_ratio, 1),
          'for validation. Big brain')
    # create train and validation folders
    for label in labels:
        for split in splits:
            directory = split + '/' + label
            if not os.path.exists(directory):
                os.makedirs(split + '/' + label)

        # take images with current label and shuffle them
        images = os.listdir(label)
        np.random.shuffle(images)

        train_images, validation_images = np.split(np.array(images),
                                                   [int(train_ratio * len(images))])

        train_images = [label + '/' + name for name in train_images.tolist()]
        validation_images = [label + '/' + name for name in validation_images.tolist()]

        print('\nTotal images for', label, ':', len(images))
        print('Training:', len(train_images))
        print('Validation:', len(validation_images))

        NB_TRAIN_IMG += len(train_images)
        NB_VALID_IMG += len(validation_images)
        # save images in train and validation directories
        for name in train_images:
            directory = 'train/' + label
            shutil.copy2(name, directory)

        for name in validation_images:
            directory = 'validation/' + label
            shutil.copy2(name, directory)

    # remove the folders saved previously (see @method get_images)
    remove_images(labels)
    print('\nsplit\nayyyy\n')
    return NB_TRAIN_IMG, NB_VALID_IMG


#################################           B E W A R E            ####################################################
#################################    CONVOLUTIAL NEURAL NETWORK    ####################################################

def CNN():
    IMG_SIZE = 256
    NB_CHANNELS = 3
    NB_EPOCHS = 5
    BATCH_SIZE = 3
    print('CNN will look for', labels, '\nBatch size:', BATCH_SIZE, '\nNumber of epochs:', NB_EPOCHS)

    # split and get number of images for train and validation
    NB_TRAIN_IMG, NB_VALID_IMG = train_validation_split()
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
    cnn.add(Dense(len(labels)))
    cnn.add(Activation('softmax'))

    # load previously stored weights
    try:
        cnn.load_weights('cnn_baseline.h5')
        print('Using previously stored weights. *beware, the CNN might have been trained on different labels*')
    except:
        'error'
        print('Initialising weights')
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
        epochs=NB_EPOCHS,
        validation_data=validation_generator,
        validation_steps=NB_VALID_IMG // BATCH_SIZE)
    end = time.time()

    print('Processing time:', (end - start) / 60)
    print('CNN is tired')

    # Save weights
    cnn.save_weights('cnn_baseline.h5')

    # Remove contents of the train and validation directories
    remove_images(splits)


get_images()
CNN()
remove_images(labels)

print('############################## U DID IT ############################################################')
