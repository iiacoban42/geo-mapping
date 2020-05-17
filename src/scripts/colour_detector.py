"""Module for extracting colors from the tiles"""
import os
import urllib.request
import extcolors


# pylint: disable=C0301
def extract_colors(name):
    """Run extcolors on the input image (now it runs on black_tile.jpg to exemplify behavior)"""
    result = []
    if os.path.exists(name):
        colors, pixel_count = extcolors.extract(name)
        # extcolors.print_result(colors, pixel_count)
        for (color, pixels) in colors:
            result.append((color, round(pixels / pixel_count * 100, 2)))
    return result


def get_tile(year, result):
    """Fetching map tiles"""
    for x_coord in range(75077, 75825):
        for y_coord in range(74956, 75879):
            res = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + str(
                year) + "/MapServer/tile/11/" + str(y_coord) + "/" + str(x_coord)
            urllib.request.urlretrieve(res, "tile.png")
            tile = extract_colors("tile.png")
            print(tile)
            result.append(tile)


def get_map(year):
    """Fetch tiles from map and extract the colors"""
    result_year = []

    get_tile(year, result_year)

    print(result_year)

# get_map(2016)
