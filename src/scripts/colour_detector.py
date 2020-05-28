"""Module for extracting colors from the tiles"""
import os
import extcolors


# pylint: disable=C0301
def extract_colors(name):
    """Run extcolors on the input image (now it runs on black_tile.jpg to exemplify behavior)"""
    result = []
    if os.path.exists(name):
        colors, pixel_count = extcolors.extract(name)
        # for each colour, calculate what percentage of the image is that specific colour
        for (color, pixels) in colors:
            result.append((color, round(pixels / pixel_count * 100, 2)))
    return result

