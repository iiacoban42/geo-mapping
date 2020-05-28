"""Tile filtering script"""
import os
import cv2
import numpy as np


# pylint: disable=all
# suppress cv2 has no imread member

def delete_img(img):
    """delete all tile identical to the black/empty tile in the current directory"""
    original = cv2.imread("black_tile.png")
    dup = cv2.imread(img)

    if not np.bitwise_xor(original, dup).any():
        os.remove(img)
    else:
        return


def cleanup():
    """Runs delete_img on all files in the current directory"""
    directory = os.fsencode("../../..")
    for file in os.listdir(directory):
        F = str(file).replace("'", '')
        F = F.replace('b', '')
        delete_img(F)
