"""Tile filtering script"""
import os
import cv2
import numpy as np


# pylint: disable=all
# suppress cv2 has no imread member

def delete_img(img):
    """delete all tile identical to the black/empty tile in the current directory"""
    # print("img"+img)
    original = cv2.imread("black_tile.png")
    dup = cv2.imread(img)

    if not np.bitwise_xor(original, dup).any():
        os.remove(img)
    else:
        return


directory = os.fsencode("../../..")
for file in os.listdir(directory):
    # print("f:"+str(file))
    F = str(file).replace("'", '')
    F = F.replace('b', '')
    # print(""+f)
    delete_img(F)
