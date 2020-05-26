"""Module for assigning labels to tiles based on colours"""
import os
import extcolors


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

def extract_colours(name):
    """Run extcolors on the input image (now it runs on black_tile.jpg to exemplify behavior)"""
    result = []
    if os.path.exists(name):
        colors, pixel_count = extcolors.extract(name)
        for (color, pixels) in colors:
            result.append((color, round(pixels / pixel_count * 100, 2)))
    return result


def sort_tiles():
    """Check each file in the images directory and assign labels based on colours"""
    for file in os.listdir("images"):
        print(file)
        result = extract_colours("images/" + file)
        w_g_b = 0.0  # % of white/gray/black
        b_t = 0.0  # % of blue/teal
        o = 0.0  # % of other colours
        labels = []
        for tuple in result:
            colour = find_colour(tuple[0])
            if tuple[1] > 75.0:
                if colour == "blue" or colour == "teal":
                    labels.append("water")
                elif colour == "white" or colour == "black" or colour == "gray":
                    labels.append("building")
                else:
                    labels.append("land")
            elif colour == "white" or colour == "black" or colour == "gray":
                w_g_b += tuple[1]
            elif colour == "blue" or colour == "teal":
                b_t += tuple[1]
            else:
                o += tuple[1]
        if w_g_b > 2.0 and not labels.__contains__("building"):
            labels.append("building")
        if b_t > 2.0 and not labels.__contains__("water"):
            labels.append("water")
        if o > 20.0 and not labels.__contains__("land"):
            labels.append("land")
        labels.sort()
        dir_name = labels[0]
        for label in labels[1:]:
            dir_name += "+" + label
        os.replace("images/" + file, "labels/" + dir_name + "/" + file)


def find_colour(rgb):
    """Compare given rgb triplet to predefined colours to find the closest one"""
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
    gray = 1
    differences = [abs(rgb[0] - rgb[1]), abs(rgb[1] - rgb[2]), abs(rgb[2] - rgb[1])]
    for diff in differences:
        if diff > 10:
            gray = 0
    if gray == 1:
        return "gray"
    min_dist = 30000
    nearest_colour = ""
    for colour in colours:
        # euclidean distance
        d = pow((colour[0] - rgb[0]), 2) + pow((colour[1] - rgb[1]), 2) + pow(
            (colour[2] - rgb[2]), 2)
        if d < min_dist:
            min_dist = d
            nearest_colour = colours[colour]
    return nearest_colour


sort_tiles()
