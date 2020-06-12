# folder structure needs to be as follows:
# in the same folder as this script add 2 folders: train and validation
# both have folders: building, land, water
# in train put training images
# in validation put validation images
import os
import shutil
import urllib

import numpy as np
from keras.layers import Activation, Flatten, Dense, Dropout
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.preprocessing import image

from core.models import AI_Characteristics as PredictionsTable
from core.models import AI_Tiles as AITilesTable
from core.models import Dataset as DatasetTable

os.chdir('detection')

labels = ['building', 'land', 'water']
splits = ['train', 'validation']


#######################################    HELPER FUNCTIONS    ########################################################

# saves ai classification in the database
def save_labels(tile_x, tile_y, tile_year, building, land, water):
    tile = AITilesTable(x_coord=tile_x, y_coord=tile_y, year=tile_year)
    tile.save()
    prediction = PredictionsTable(tiles_id=tile, water_prediction=water, land_prediction=land,
                                  buildings_prediction=building)
    prediction.save()


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
    number = {'building': 0, 'land': 0, 'water': 0}
    max = min(DatasetTable.objects.filter(building=1, land=0, water=0).count(),
              DatasetTable.objects.filter(building=0, land=1, water=0).count(),
              DatasetTable.objects.filter(building=0, land=0, water=1).count())
    print('Maximum', max)
    for row in dataset:
        x = str(row.x_coord)
        y = str(row.y_coord)
        year = str(row.year)
        res = 'https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_' + year + '/MapServer/tile/11/' + y + '/' + x
        label = ''
        if row.building == 1:
            label += 'building'
        if row.land == 1:
            label += 'land'
        if row.water == 1:
            label += 'water'
        if labels.__contains__(label):
            number[label] += 1
            print(label, 'has', number[label])
            if not os.path.exists(label):
                os.makedirs(label)
            try:
                if number[label] < max:
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
    # remove_images(labels)
    print('\nsplit\nayyyy\n')
    return NB_TRAIN_IMG, NB_VALID_IMG


#################################           B E W A R E            ####################################################
#################################    CONVOLUTIAL NEURAL NETWORK    ####################################################

def CNN():
    IMG_SIZE = 256
    NB_CHANNELS = 3
    NB_EPOCHS = 3
    BATCH_SIZE = 3
    print('CNN will look for', labels, '\nBatch size:', BATCH_SIZE, '\nNumber of epochs:', NB_EPOCHS)

    # split and get number of images for train and validation
    NB_TRAIN_IMG, NB_VALID_IMG = train_validation_split()

    cnn = Sequential()
    cnn.add(Conv2D(filters=32,
                   kernel_size=(2, 2),
                   strides=(1, 1),
                   padding='same',
                   input_shape=(IMG_SIZE, IMG_SIZE, NB_CHANNELS),
                   data_format='channels_last'))
    cnn.add(Activation('relu'))
    cnn.add(MaxPooling2D(pool_size=(2, 2),
                         strides=2))
    cnn.add(Conv2D(filters=64,
                   kernel_size=(2, 2),
                   strides=(1, 1),
                   padding='valid'))
    cnn.add(Activation('relu'))
    cnn.add(MaxPooling2D(pool_size=(2, 2),
                         strides=2))
    cnn.add(Flatten())
    cnn.add(Dense(64))
    cnn.add(Activation('relu'))
    cnn.add(Dropout(0.15))
    cnn.add(Dense(len(labels)))
    cnn.add(Activation('softmax'))
    cnn.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    # load previously stored weights
    try:
        cnn.load_weights('cnn_baseline.h5')
        print('Using previously stored weights. *beware, the CNN might have been trained on different labels*')
    except:
        'error'
        print('Initialising weights')
    cnn.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    # print('Processing time:', (end - start) / 60)
    print('CNN is tired')

    for label in labels:
        images = os.listdir('validation' + '/' + label)
        for img in images:
            tile_y, tile_x = img.replace(".png", "").split("_")
            name = "validation/" + label + "/" + img
            img = image.load_img(name)
            img = image.img_to_array(img)
            img = img.reshape((1,) + img.shape)

            # add 0.1 in case there might be 2 labels (softmax gives the sum of the labels = 1),
            # therefore the chance of having a tile with 2 labels classified as 0.5, 0.5, 0 is quite rare
            building = round(cnn.predict(img)[0][0])
            land = round(cnn.predict(img)[0][1] + 0.1)
            water = round(cnn.predict(img)[0][2] + 0.1)
            # if building + water + land == 2:
            #     print(building, land, water)
            #     print(name, '         is', label, 'classified', labels[int(cnn.predict_classes(img))], '\n\n')
            save_labels(tile_x, tile_y, 2016, building, land, water)


# print("\n\ntest generator\n\n")
# test_generator = test_datagen.flow_from_directory(
#     'validation',
#     target_size=(IMG_SIZE, IMG_SIZE),
#     color_mode='rgb',
#     shuffle=True,
#     class_mode='categorical',
#     batch_size=BATCH_SIZE)
# filenames = test_generator.filenames
# nb_samples = len(filenames)
# prediction = cnn.predict_generator(test_generator, steps=nb_samples)
# print(prediction)
# with open('predictions.txt', 'w') as f:
#     csv.writer(f, delimiter=' ').writerows(prediction)
#
# Remove contents of the train and validation directories
# remove_images(splits)


# get_images()
CNN()
# remove_images(labels)

print('############################## U DID IT ############################################################')
