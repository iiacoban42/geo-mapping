"""Module for extracting colors from the tiles"""
import extcolors
import urllib.request


def extract_colors():
    """Run extcolors on the input image (now it runs on tile.jpg to exemplify behavior)"""
    colors, pixel_count = extcolors.extract("tile.jpg")
    # extcolors.print_result(colors, pixel_count)
    result = []
    for (color, pixels) in colors:
        result.append((color, round(pixels / pixel_count * 100, 2)))
    return result


def get_tile(year, result):
    for x_coord in range(75077, 75825):
        for y_coord in range(74956, 75879):
            res = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + str(
                year) + "/MapServer/tile/11/" + str(y_coord) + "/" + str(x_coord)
            urllib.request.urlretrieve(res, "tile.jpg")
            tile = extract_colors()
            print(tile)
            result.append(tile)


def get_map(year):
    result_year = []

    get_tile(year, result_year)

    print(result_year)


get_map(2016)
