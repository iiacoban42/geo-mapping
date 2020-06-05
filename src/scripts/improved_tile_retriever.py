import urllib.request
from PIL import Image

from core.models import UsableTiles as UsableTilesTable

pix_to_check = []

for i in range(0, 256):
    pix_to_check.append(i)

for i in range(1, 256):
    pix_to_check.append(i * 256)

for i in range(1, 256):
    pix_to_check.append(256 * i + i)

pix_to_check.sort()


def save_all_tiles(year, range_x, range_y):
    for x_coord in range_x:
        for y_coord in range_y:
            res = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + str(
                year) + "/MapServer/tile/11/" + str(y_coord) + "/" + str(x_coord)
            # print(res)
            check_request(res, year, x_coord, y_coord)
    return "success"


def check_request(res, year, x_coord, y_coord):
    try:
        file = urllib.request.urlopen(res)
        im = Image.open(file, 'r')
        finish_request(im, year, x_coord, y_coord)
    except:
        print("url was invalid")


def finish_request(im, year, x_coord, y_coord):
    pix_val = list(im.getdata())
    if not check_transparent(pix_val):
        if not check_full_white(pix_val):
            # print("found one")
            save_tile(year, x_coord, y_coord)


def check_transparent(pix_val):
    # check all 4 corners
    # if one of them has an alpha value, it is transparent
    # discard transparent images
    if len(pix_val[0]) < 4 and \
            len(pix_val[255]) < 4 and \
            len(pix_val[65280]) < 4 and \
            len(pix_val[65535]) < 4:
        return False
    else:
        return True


def check_full_white(pix_val):
    count = 0
    for pix in pix_to_check:
        if pix_val[pix] == (255, 255, 255):
            count += 1
    # if at least 74% of counted pixels are white, consider the entire image to be white
    if count >= 575:
        return True
    else:
        return False


def save_tile(year, x_coord, y_coord):
    tile = UsableTilesTable(x_coord=x_coord, y_coord=y_coord, year=year)
    tile.save()

# import timeit
#
# start = timeit.default_timer()
#
# save_all_tiles(2010, range(75079, 75804), range(74990, 76568))
#
# stop = timeit.default_timer()
#
# print('Time: ', stop - start)
#
# save_all_tiles(2010, range(75300, 75804), range(75300, 76568))
