"""Module for saving useful tiles into the database"""
import urllib.request

from PIL import Image

from core.models import UsableTiles as UsableTilesTable

# note: this module saves the coordinates of valid tiles to the database
# it can relatively easily be modified to save them locally,
# if that is deemed as a more suitable solution
# we saved coordinates from 1950, 2010 and 2013-2016 in the database
# these were used to run the classification on

# these are the pixels that need to be checked,
# in order to determine if the image is fully white
# the pixels checked are the ones on the first row,
# first column, and main diagonal of the image
# note: all of the pixels could be checked,
# but that would be considerably slower
pix_to_check = []

for i in range(0, 256):
    pix_to_check.append(i)

for i in range(1, 256):
    pix_to_check.append(i * 256)

for i in range(1, 256):
    pix_to_check.append(256 * i + i)

pix_to_check.sort()

# for each given year, there is an array which contains two ranges
# the first range is the one for the x coordinate
# the second range is the one for the y coordinate
# these are taken in the order from
# https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services?f=html&cacheKey=bc1d3b3824ba27e0
year_coordinates = {
    "1950": [range(75084, 75809), range(74932, 76568)],
    "1975": [range(75043, 75816), range(74978, 76568)],
    "1901": [range(75086, 75790), range(74947, 75851)],
    "1925": [range(75074, 75819), range(74931, 75872)],
    "1910": [range(75086, 75790), range(74947, 75851)],
    "1980": [range(75076, 75812), range(74983, 76568)],
    "1850": [range(74969, 75882), range(74891, 76043)],
    "1900": [range(75086, 75790), range(74947, 75851)],
    "1815": [range(75072, 75961), range(74948, 75686)],
    "1868": [range(74969, 75882), range(74891, 76043)],
    "1915": [range(75086, 75790), range(74947, 75851)],
    "1970": [range(75045, 75825), range(74975, 76568)],
    "1940": [range(75060, 75823), range(74914, 76568)],
    "2000": [range(75077, 75796), range(74999, 76568)],
    "1930": [range(75086, 75812), range(74906, 75893)],
    "1960": [range(75068, 75830), range(74959, 76568)],
    "1990": [range(75042, 75802), range(74993, 76568)],
    "1920": [range(75086, 75796), range(74955, 75843)],
    "2010": [range(75079, 75804), range(74990, 76568)],
    "1935": [range(75086, 75812), range(74906, 76556)],
    "1945": [range(75086, 75822), range(74925, 76568)],
    "1995": [range(75042, 75810), range(74993, 76568)],
    "1955": [range(75068, 75830), range(74956, 76568)],
    "1965": [range(75044, 75815), range(74977, 76568)],
    "1880": [range(74969, 75882), range(74891, 76043)],
    "2005": [range(75081, 75805), range(74993, 76568)],
    "2015": [range(75077, 75825), range(74956, 76556)],
    "2014": [range(75077, 75805), range(74988, 76568)],
    "1985": [range(75062, 75804), range(74994, 76568)],
    "1865": [range(74969, 75882), range(74891, 76043)],
    "1822": [range(75072, 75961), range(74948, 75686)],
    "2011": [range(75079, 75804), range(74990, 76568)],
    "1860": [range(74969, 75882), range(74891, 76043)],
    "1870": [range(74969, 75882), range(74891, 76043)],
    "1933": [range(75086, 75812), range(74906, 75893)],
    "1947": [range(75086, 75822), range(74925, 76568)],
    "1877": [range(74969, 75882), range(74891, 76043)],
    "1988": [range(75068, 75807), range(74991, 76568)],
    "1890": [range(75079, 75793), range(74956, 75833)],
    "2012": [range(75076, 75806), range(74988, 76568)],
    "1820": [range(74969, 75881), range(74891, 76192)],
    "1984": [range(75062, 75804), range(74994, 76568)],
    "1831": [range(74969, 75882), range(74891, 76043)],
    "1832": [range(74969, 75882), range(74891, 76043)],
    "1833": [range(74969, 75882), range(74891, 76043)],
    "1834": [range(74969, 75882), range(74891, 76043)],
    "1835": [range(74969, 75882), range(74891, 76043)],
    "1836": [range(74969, 75882), range(74891, 76043)],
    "1837": [range(74969, 75882), range(74891, 76043)],
    "1838": [range(74969, 75882), range(74891, 76043)],
    "1839": [range(74969, 75882), range(74891, 76043)],
    "1840": [range(74969, 75882), range(74891, 76043)],
    "1841": [range(74969, 75882), range(74891, 76043)],
    "1842": [range(74969, 75882), range(74891, 76043)],
    "1843": [range(74969, 75882), range(74891, 76043)],
    "1844": [range(74969, 75882), range(74891, 76043)],
    "1845": [range(74969, 75882), range(74891, 76043)],
    "1846": [range(74969, 75882), range(74891, 76043)],
    "1847": [range(74969, 75882), range(74891, 76043)],
    "1848": [range(74969, 75882), range(74891, 76043)],
    "1849": [range(74969, 75882), range(74891, 76043)],
    "1966": [range(75044, 75815), range(74977, 76568)],
    "1978": [range(75049, 75816), range(74981, 76568)],
    "1823": [range(75072, 75961), range(74948, 75686)],
    "1824": [range(75072, 75961), range(74948, 75686)],
    "1825": [range(75072, 75961), range(74948, 75686)],
    "1826": [range(75072, 75961), range(74948, 75686)],
    "1827": [range(75072, 75961), range(74948, 75686)],
    "1828": [range(75072, 75961), range(74948, 75686)],
    "1829": [range(75072, 75961), range(74948, 75686)],
    "1875": [range(74969, 75882), range(74891, 76043)],
    "1905": [range(75086, 75790), range(74947, 75851)],
    "1981": [range(75050, 75808), range(74983, 76568)],
    "1816": [range(74969, 75881), range(74891, 76192)],
    "1817": [range(74969, 75881), range(74891, 76192)],
    "1818": [range(74969, 75881), range(74891, 76192)],
    "1819": [range(74969, 75881), range(74891, 76192)],
    "1999": [range(75081, 75801), range(74992, 76568)],
    "1998": [range(75081, 75801), range(74992, 76568)],
    "2009": [range(75079, 75804), range(74990, 76568)],
    "1992": [range(75042, 75792), range(74993, 76568)],
    "1991": [range(75042, 75802), range(74993, 76568)],
    "1982": [range(75050, 75808), range(74983, 76568)],
    "1851": [range(74969, 75882), range(74891, 76043)],
    "2001": [range(75077, 75796), range(74999, 76568)],
    "1918": [range(75086, 75796), range(74955, 75843)],
    "1989": [range(75042, 75807), range(74991, 76568)],
    "1954": [range(75068, 75830), range(74956, 76568)],
    "1909": [range(75086, 75790), range(75086, 75851)],
    "1899": [range(75086, 75810), range(74955, 75842)],
    "2013": [range(75079, 75803), range(74991, 76568)],
    "1885": [range(74969, 75882), range(74891, 76043)],
    "1956": [range(75068, 75830), range(74956, 76568)],
    "2006": [range(75079, 75804), range(74990, 76568)],
    "1941": [range(75060, 75823), range(74914, 76568)],
    "1973": [range(75043, 75816), range(74978, 76568)],
    "2016": [range(75077, 75825), range(74956, 75879)],
    "1963": [range(75044, 75815), range(74977, 76568)],
}


def save_all_tiles(year, range_x, range_y):
    """save all the tiles for the given year to the database"""
    for x_coord in range_x:
        for y_coord in range_y:
            if y_coord % 10 == 0:
                # get this table once every 10 iterations to avoid losing connection to database
                # Note: this is horrible and slow, but I have no idea how to do it differently - Andrei
                tile1 = UsableTilesTable.objects.all()
            res = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + str(
                year) + "/MapServer/tile/11/" + str(y_coord) + "/" + str(x_coord)
            # call the method that tried to fetch the tile's image from the tile server
            check_request(res, year, x_coord, y_coord)
    return "success"


def check_request(res, year, x_coord, y_coord):
    """try to fetch the tile's image from the tile server"""
    # this might either result in a HTTP 404 if the url is invalid
    # or in a MySQL error, if the connection to the database is lost
    try:
        file = urllib.request.urlopen(res)
        im = Image.open(file, 'r')
        finish_request(im, year, x_coord, y_coord)
    except Exception as e:
        print(e)


def finish_request(im, year, x_coord, y_coord):
    """finish the request, by checking if the image is white or transparent"""
    pix_val = list(im.getdata())
    if not check_transparent(pix_val):
        if not check_full_white(pix_val):
            print("image was good. saving...")
            save_tile(year, x_coord, y_coord)
            print("saved")


def check_transparent(pix_val):
    """check if the image is transparent"""
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
    """check if the image if fully white"""
    # count how many of the check pixels are white
    count = 0
    for pix in pix_to_check:
        if pix_val[pix] == (255, 255, 255):
            count += 1
    # if at least 75% of counted pixels are white, consider the entire image to be white
    if count >= 575:
        return True
    else:
        return False


def save_tile(year, x_coord, y_coord):
    """save the tile to the database"""
    tile = UsableTilesTable(x_coord=x_coord, y_coord=y_coord, year=year)
    tile.save()


def run(year):
    """run the entire process on the given year"""
    # check if the year was provided as an int
    # if so, cast it into a string, since the key
    # in a dictionary must be a string
    if isinstance(year, int):
        year = str(year)
    # if the year was not provided as an int, nor as a string,
    # ask the user to do so and return nothing
    elif not isinstance(year, str):
        print("Please provide the year as either an int or a string")
        print("What you provided was a " + str(type(year)))
        return
    # check if the given year is in the dictionary
    # if it is not, present a list of possible years
    if not year_coordinates.__contains__(year):
        print("The provided year does not exist on the tile server")
        print("Pick one of the following years:")
        years = ""
        for key, value in year_coordinates.items():
            years += key + " "
        print(years)
        return
    # if the given year is in the dictionary, continue with saving its tiles
    else:
        range_x = year_coordinates.get(year)[0]
        range_y = year_coordinates.get(year)[1]
        save_all_tiles(year, range_x, range_y)

