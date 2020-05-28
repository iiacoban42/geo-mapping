"""Tile filtering script"""
import imghdr
import os
import cv2
import numpy as np

# pylint: disable=all
# suppress cv2 has no imread member
from PIL.Image import Image


def delete_img(img, original):
    """delete all tile identical to the black/empty tile in the current directory"""
    if os.path.exists(img):

        # check that the file is a valid png
        if imghdr.what(img) != "png":
            return "file is not a valid png"

        # open the image
        original = cv2.imread(original)
        dup = cv2.imread(img)


        # compare image with an entirely black image
        if not np.bitwise_xor(original, dup).any():
            os.remove(img)
            return "successfully removed"
        else:
            return "image was not black"
    else:
        return "file does not exist"


def cleanup(directory, original):
    """Runs delete_img on all files in the current directory and corrects file naming errors"""
    # directory = os.fsencode("../../..")
    # print(directory)
    for file in os.listdir(directory):
        # fil = str(file).replace("'", '')
        # fil = fil.replace('b', '')
        print(file)
        delete_img(directory + "/" + file, original)

