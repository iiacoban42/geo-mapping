"""Module for retrieving map tiles"""
import urllib.request


# pylint: disable=C0301

def get_map(year, range_x, range_y, folder):
    """Fetching map tiles"""

    # valid tile range
    # ideally run several scripts with different ranges to speed up
    for x_coord in range_x:
        for y_coord in range_y:
            res = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + str(
                year) + "/MapServer/tile/11/" + str(y_coord) + "/" + str(x_coord)
            urllib.request.urlretrieve(res, "../" + folder + "/" + str(y_coord) + "_" + str(x_coord) + ".png")
