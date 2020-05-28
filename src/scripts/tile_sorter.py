"""Module for assigning labels to tiles based on colours"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname("src"), '..'))
from src.scripts import colour_detector


# usage: place script in the same folder as 2 other directories names images and labels
#        images contains the tiles
#        labels has subdirectories with all possible combinations of labels:
#               -building
#               -building+land
#               -building+land+water
#               -building+water
#               -land
#               -land+water
#               -water
# note: the names of the directories have to be exactly those above, otherwise the script will crash
# since it cannot find the specified directory


def sort_tiles(image_directory, labels_directory):
    """Check each file in the images directory and assign labels based on colours"""
    for file in os.listdir(image_directory):
        result = colour_detector.extract_colours(image_directory + "/" + file)
        w_g_b = 0.0  # % of white/gray/black
        b_t = 0.0  # % of blue/teal
        o = 0.0  # % of other colours
        labels = []
        for tuple in result:
            colour = find_colour(tuple[0])
            # check if there is a dominant colour
            if tuple[1] > 75.0:
                # if colour is blue or teal, assign the water label
                if colour == "blue" or colour == "teal":
                    labels.append("water")
                # if colour is white, gray or black, assign the building label
                elif colour == "white" or colour == "black" or colour == "gray":
                    labels.append("building")
                # if colour is a different one from those above, consider it land
                else:
                    labels.append("land")
            # if there is no dominant colour, add up percentages of those 3 categories of colours defined above
            elif colour == "white" or colour == "black" or colour == "gray":
                w_g_b += tuple[1]
            elif colour == "blue" or colour == "teal":
                b_t += tuple[1]
            else:
                o += tuple[1]
        # check percentages of the colours that were added up above
        # if they cross a certain percentage threshold, assign a corresponding label
        # note: these threshold percentages are difficult to optimize to work properly on every image
        #       since there are sometimes black lines crossing the image that get counted as buildings
        if w_g_b > 2.0 and not labels.__contains__("building"):
            labels.append("building")
        if b_t > 2.0 and not labels.__contains__("water"):
            labels.append("water")
        if o > 20.0 and not labels.__contains__("land"):
            labels.append("land")

        # sort the labels alphabetically, in order to form the name of the folder that the image needs to be placed in
        labels.sort()
        dir_name = labels[0]
        for label in labels[1:]:
            dir_name += "+" + label
        os.replace(image_directory + "/" + file, labels_directory + "/" + dir_name + "/" + file)


def find_colour(rgb):
    """Compare given rgb triplet to predefined colours to find the closest one"""

    # this cannot normally happen to an image that is processed automatically, since colours
    # are rbg by default, but it can happen if the function is called with invalid values
    if rgb[0] < 0 or rgb[0] > 255 or rgb[1] < 0 or rgb[1] > 255 or rgb[2] < 0 or rgb[2] > 255:
        return "part of the rgb triplet was invalid"

    # dictionary of predefined colours
    colours = {
        (255, 0, 0): "red",
        (255, 100, 100): "red",
        (200, 100, 100): "red",
        (150, 0, 0): "red",
        (150, 50, 50): "red",
        (50, 0, 0): "red",
        (0, 255, 0): "green",
        (100, 255, 100): "green",
        (100, 200, 100): "green",
        (0, 150, 0): "green",
        (50, 150, 50): "green",
        (0, 50, 0): "green",
        (0, 0, 255): "blue",
        (100, 100, 255): "blue",
        (100, 100, 200): "blue",
        (0, 0, 150): "blue",
        (50, 50, 150): "blue",
        (0, 0, 50): "blue",
        (255, 255, 0): "yellow",
        (255, 255, 100): "yellow",
        (200, 200, 100): "yellow",
        (150, 150, 0): "yellow",
        (150, 150, 50): "yellow",
        (50, 50, 0): "yellow",
        (247, 248, 232): "yellow",  # light yellow colour used on most of the map
        (233, 231, 182): "yellow",  # darker yellow used in some places
        (255, 0, 255): "magenta",
        (255, 100, 255): "magenta",
        (200, 100, 200): "magenta",
        (150, 0, 150): "magenta",
        (150, 50, 150): "magenta",
        (50, 0, 50): "magenta",
        (0, 255, 255): "teal",
        (100, 255, 255): "teal",
        (100, 200, 200): "teal",
        (0, 150, 150): "teal",
        (50, 150, 150): "teal",
        (0, 50, 50): "teal",
        (232, 248, 248): "teal",  # light blue-ish colour used for water in some places
        (255, 255, 255): "white",
        (0, 0, 0): "black"
    }
    # calculate euclidean distance to all of the predefined colours
    # pick the closest one
    # note: 30000 was arbitrarily chosen as a threshold for a "close enough" colour
    #       i.e. if a distance is greater than that it cannot reasonably be considered closest,
    #       even if it is the smallest distance, though it should be quite unlikely to happen,
    #       due to the number of predefined colours
    min_dist = 30000
    nearest_colour = ""

    for colour in colours:
        # euclidean distance
        d = pow((colour[0] - rgb[0]), 2) + pow((colour[1] - rgb[1]), 2) + pow(
            (colour[2] - rgb[2]), 2)
        if d < min_dist:
            min_dist = d
            nearest_colour = colours[colour]

    # colour is considered gray if the r g b values are all within 10 of each other
    gray = 1
    differences = [abs(rgb[0] - rgb[1]), abs(rgb[1] - rgb[2]), abs(rgb[2] - rgb[1])]
    for diff in differences:
        if diff > 10:
            gray = 0
    if gray == 1 and rgb[0] != 0 and rgb[1] != 0 and rgb[2] != 0 and rgb[0] != 255 and rgb[1] != 255 and rgb[2] != 255:
        return "gray"

    return nearest_colour

