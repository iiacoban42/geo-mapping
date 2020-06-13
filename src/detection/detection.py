# folder structure needs to be as follows:
# in the same folder as this script add 2 folders: train and validation
# both have folders: building, land, water
# in train put training images
# in validation put validation images
import os
import shutil
import time
import urllib

import keras
import numpy as np
from keras.layers import Activation, Flatten, Dense, Dropout
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.preprocessing import image
from keras_preprocessing.image import ImageDataGenerator
from skimage import io

from core.models import AI_Characteristics as PredictionsTable
from core.models import AI_Tiles as AITilesTable
from core.models import Dataset as DatasetTable
from core.models import UsableTiles as PredictUsableTiles

os.chdir('detection')

labels = ['building', 'land', 'water']
splits = ['train', 'validation']


#######################################    HELPER FUNCTIONS    ########################################################

# saves ai classification in the database
def save_labels(tile_x, tile_y, tile_year, building, land, water):
    if AITilesTable.objects.filter(x_coord=tile_x, y_coord=tile_y).count() > 0:
        tile = AITilesTable.objects.filter(x_coord=tile_x, y_coord=tile_y).first()
        print('Already existing ==> update', tile)

    else:
        tile = AITilesTable(x_coord=tile_x, y_coord=tile_y, year=tile_year)
        tile.save()
        print('New discovery such wow', tile)
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
def get_images_train(table=DatasetTable):
    print('This will take a while..')
    dataset = table.objects.all()
    number = {'building': 0, 'land': 0, 'water': 0}
    max = min(DatasetTable.objects.filter(building=1, land=0, water=0).count(),
              DatasetTable.objects.filter(building=0, land=1, water=0).count(),
              DatasetTable.objects.filter(building=0, land=0, water=1).count())
    print('Maximum', max, "images for each label")
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
                # avoid being biased towards a label which has more images than the rest
                if number[label] < max:
                    urllib.request.urlretrieve(res, label + '/' + y + '_' + x + '.png')
            except:
                'not found'
                print('Tile from', year, 'having x=', x, 'and y=', y, 'is not on the website. Delete it.\n')
    print('\ndatabase hacked\n')


# split the images in two sets: train and validation
# result: train/building, train/water, train/buildingwater... (same for validation)
def train_validation_split():
    number_train = 0
    number_validation = 0
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

        number_train += len(train_images)
        number_validation += len(validation_images)
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
    return number_train, number_validation


#################################           B E W A R E            ####################################################
#################################    CONVOLUTIAL NEURAL NETWORK    ####################################################
class CNN:
    def __init__(self, image_size=256, number_channels=3, number_epochs=5, batch_size=6):
        self.image_size = image_size
        self.number_channels = number_channels
        self.number_epochs = number_epochs
        self.batch_size = batch_size
        print('CNN will look for', labels, '\nBatch size:', self.batch_size, '\nNumber of epochs:', self.number_epochs)
        try:
            self.model = keras.models.load_model('model')
        except:
            "not loaded"
            self.model = Sequential()
            self.model.add(Conv2D(filters=32,
                                  kernel_size=(2, 2),
                                  strides=(1, 1),
                                  padding='same',
                                  input_shape=(self.image_size, self.image_size, self.number_channels),
                                  data_format='channels_last'))
            self.model.add(Activation('relu'))
            self.model.add(MaxPooling2D(pool_size=(2, 2),
                                        strides=2))
            self.model.add(Conv2D(filters=64,
                                  kernel_size=(2, 2),
                                  strides=(1, 1),
                                  padding='valid'))
            self.model.add(Activation('relu'))
            self.model.add(MaxPooling2D(pool_size=(2, 2),
                                        strides=2))
            self.model.add(Flatten())
            self.model.add(Dense(64))
            self.model.add(Activation('relu'))
            self.model.add(Dropout(0.2))
            self.model.add(Dense(len(labels)))
            self.model.add(Activation('softmax'))
            self.model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
            self.model.summary()

    def train(self):
        # split and get number of images for train and validation
        number_train, number_validation = train_validation_split()

        train_datagen = ImageDataGenerator(horizontal_flip=True, rotation_range=90)
        validation_datagen = ImageDataGenerator(horizontal_flip=True, rotation_range=90)

        train_generator = train_datagen.flow_from_directory(
            'train',
            target_size=(self.image_size, self.image_size),
            class_mode='categorical',
            batch_size=self.batch_size)

        validation_generator = validation_datagen.flow_from_directory(
            'validation',
            target_size=(self.image_size, self.image_size),
            class_mode='categorical',
            batch_size=self.batch_size)

        start = time.time()
        self.model.fit_generator(
            train_generator,
            steps_per_epoch=number_train // self.batch_size,
            epochs=self.number_epochs,
            validation_data=validation_generator,
            validation_steps=number_validation // self.batch_size)
        end = time.time()
        self.model.save("model")

        print('Processing time:', (end - start) / 60)
        print('CNN is tired')
        remove_images(splits)

    def predict(self, table=PredictUsableTiles):
        tiles = table.objects.all()
        for row in tiles:
            x = str(row.x_coord)
            y = str(row.y_coord)
            year = str(row.year)
            URL = 'https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_' + year + '/MapServer/tile/11/' + y + '/' + x
            img = io.imread(URL)
            img = image.img_to_array(img)
            img = img.reshape((1,) + img.shape)

            # add 0.1 in case there might be 2 labels (softmax gives the sum of the labels = 1),
            # therefore the chance of having a tile with 2 labels classified as 0.5, 0.5, 0 is quite rare
            building = round(self.model.predict(img)[0][0] + 0.1)
            land = round(self.model.predict(img)[0][1] + 0.1)
            water = round(self.model.predict(img)[0][2] + 0.1)
            print(URL, '\n', self.model.predict(img), labels[int(self.model.predict_classes(img))], '\n')
            save_labels(x, y, year, building, land, water)


#
# get_images_train()
cnn = CNN()
# cnn.train()
cnn.predict()

print('############################## U DID IT ############################################################')
