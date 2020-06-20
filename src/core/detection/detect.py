# folder structure needs to be as follows:
# in the same folder as this script add 2 folders: train and validation
# both have folders: building, land, water
# in train put training images
# in validation put validation images
import os
import shutil
import time
import urllib

import matplotlib.pyplot as plt
import numpy as np
from django.utils import timezone
from keras.layers import Activation, Flatten, Dense, Dropout
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.preprocessing import image
from keras_preprocessing.image import ImageDataGenerator
from skimage import io

from core.models import AI_Characteristics as PredictionsTable
from core.models import AI_Tiles as AITilesTable
from core.models import Confirmed_Captcha_Characteristics as ConfirmedCaptchaChars
from core.models import Dataset as DatasetTable
from core.models import UsableTiles as PredictUsableTiles

labels = ['building', 'land', 'water']
splits = ['train', 'validation']


#######################################    HELPER FUNCTIONS    ########################################################

# saves ai classification in the database
def save_labels(tile_x, tile_y, tile_year, building, land, water):
    tile = AITilesTable.objects.filter(x_coord=tile_x, y_coord=tile_y, year=tile_year).first()
    if tile is None:
        tile = AITilesTable(x_coord=tile_x, y_coord=tile_y, year=tile_year)

    tile.save()
    prediction = PredictionsTable(tiles_id=tile, water_prediction=water, land_prediction=land,
                                  buildings_prediction=building, timestamp=timezone.now())
    prediction.save()


# removes directory and subdirectories of directory
def remove_images(directory):
    for directory in directory:
        if os.path.exists(directory):
            shutil.rmtree(directory)


# saves images from the db in folders based on their label
# see @labels
def get_images_train():
    print('This will take a while..')
    get_images_captcha()
    get_images_dataset()


def get_images_dataset():
    dataset = DatasetTable.objects.all().order_by('?')
    number = {'building': 0, 'land': 0, 'water': 0}
    max_img = min(DatasetTable.objects.filter(building=1, land=0, water=0).count(),
                  DatasetTable.objects.filter(building=0, land=1, water=0).count(),
                  DatasetTable.objects.filter(building=0, land=0, water=1).count())
    print('Maximum', max_img, "images for each dataset label")
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
            if not os.path.exists(label):
                os.makedirs(label)
            try:
                # avoid being biased towards a label which has more images than the rest...
                # e.g.: lots of water, few buildings
                if number[label] < max_img + (max_img * 0.3):
                    urllib.request.urlretrieve(res, label + '/' + y + '_' + x + '.png')
            except:
                'not found'
                print('Tile from', year, 'having x=', x, 'and y=', y, 'is not on the website. Delete it.\n')


def get_images_captcha():
    dataset = ConfirmedCaptchaChars.objects.select_related('tiles_id').all().order_by('?')
    number = {'building': 0, 'land': 0, 'water': 0}

    low_bound = 20
    high_bound = 80

    max_img = min(
        ConfirmedCaptchaChars.objects.filter(buildings_prediction__gte=high_bound, land_prediction__lte=low_bound,
                                             water_prediction__lte=low_bound).count(),
        ConfirmedCaptchaChars.objects.filter(buildings_prediction__lte=low_bound, land_prediction__gte=high_bound,
                                             water_prediction__lte=low_bound).count(),
        ConfirmedCaptchaChars.objects.filter(buildings_prediction__lte=low_bound, land_prediction__lte=low_bound,
                                             water_prediction__gte=high_bound).count())
    print('Maximum', max_img, "images for each captcha label")
    for row in dataset:
        x = str(row.tiles_id.x_coord)
        y = str(row.tiles_id.y_coord)
        year = str(row.tiles_id.year)
        res = 'https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_' + year + '/MapServer/tile/11/' + y + '/' + x
        label = ''
        if row.buildings_prediction >= high_bound:
            label += 'building'
        if row.land_prediction >= high_bound:
            label += 'land'
        if row.water_prediction >= high_bound:
            label += 'water'
        if labels.__contains__(label):
            number[label] += 1
            if not os.path.exists(label):
                os.makedirs(label)
            try:
                # avoid being biased towards a label which has more images than the rest...
                # e.g.: lots of water, few buildings
                if number[label] < max_img + (max_img * 0.3):
                    urllib.request.urlretrieve(res, label + '/' + y + '_' + x + '.png')
            except:
                'not found'
                print('Tile from', year, 'having x=', x, 'and y=', y, 'is not on the website. Delete it.\n')


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
    def __init__(self, image_size=256, number_channels=3, number_epochs=7, batch_size=12):
        self.image_size = image_size
        self.number_channels = number_channels
        self.number_epochs = number_epochs
        self.batch_size = batch_size

        print('CNN will look for', labels, '\nBatch size:', self.batch_size, '\nNumber of epochs:', self.number_epochs)

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
                              kernel_size=(4, 4),
                              strides=(1, 1),
                              padding='valid'))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.2))
        self.model.add(MaxPooling2D(pool_size=(2, 2),
                                    strides=2))
        self.model.add(Flatten())
        self.model.add(Dense(64))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.3))
        self.model.add(Dense(len(labels)))
        # using sigmoid to get the probability for each label
        self.model.add(Activation('sigmoid'))

        # load previously stored weights
        try:
            self.model.load_weights('core/detection/cnn_baseline.h5')
            print('Using previously stored weights. *beware, the CNN might have been trained on different labels*')
        except:
            'error'
            print('Initialising weights')

        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=["binary_accuracy",
                                                                                  "categorical_accuracy", 'accuracy'])
        self.model.summary()

    def train(self):
        # split and get number of images for train and validation
        number_train, number_validation = train_validation_split()
        train_datagen = ImageDataGenerator(rescale=1. / 255, zoom_range=0.2, rotation_range=90)

        validation_datagen = ImageDataGenerator(rescale=1. / 255)

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
        history = self.model.fit_generator(
            train_generator,
            steps_per_epoch=number_train // self.batch_size,
            epochs=self.number_epochs,
            validation_data=validation_generator,
            validation_steps=number_validation // self.batch_size)
        end = time.time()

        self.model.save_weights('core/detection/cnn_baseline.h5')

        # print(self.model.metrics_names)
        try:
            file = open("static/history.txt", "w")
            print(history.history["acc"])
            file.write(history.history["acc"].__str__())
            file.close()
        except:
            print('no history??')

        print('Processing time:', (end - start) / 60)
        print('CNN is tired')
        remove_images(splits)

        # summarize history for accuracy
        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.draw()
        plt.savefig('static/img/' + 'model_accuracy.png')
        plt.show()

        # summarize history for loss
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.draw()
        plt.savefig('static/img/' + 'model_loss.png')
        plt.show()

    def predict(self, predict, table):
        if predict is True:
            # take ALL tiles from the database
            tiles = table.objects.all()

            for i, row in enumerate(tiles):
                x = str(row.x_coord)
                y = str(row.y_coord)
                year = str(row.year)
                URL = 'https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_' + year + '/MapServer/tile/11/' + y + '/' + x
                img = io.imread(URL)
                img = image.img_to_array(img) / 255
                img = np.expand_dims(img, axis=0)

                # BEWARE, predicting three times
                predictions = []
                for k in range(0, len(labels)):
                    predictions.append(self.model.predict(img)[0][k])
                    # if the probability is not 0, then there is a trace of that specific feature on the tile
                    # but the labels which are not present in the image might look like: {0.00000312} (lots of decimals)
                    if predictions[k] > 0:
                        predictions[k] = 1
                    else:
                        predictions[k] = 0
                print(URL, 'building', predictions[0], 'land', predictions[1], 'water', predictions[2], '\n')
                save_labels(x, y, year, predictions[0], predictions[1], predictions[2])


def run():
    get_images_train()
    cnn = CNN()
    cnn.train()
    cnn.predict(True, PredictUsableTiles)
    print('############################## U DID IT ############################################################')
