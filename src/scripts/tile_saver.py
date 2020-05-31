"""Module for saving labeled tiles to the database"""
# pylint: disable=[import-error, unused-variable]
import os


# usage: place your "labels" folder in the same folder as this script
#        labels has subdirectories with all possible combinations of labels:
#               -building
#               -building+land
#               -building+land+water
#               -building+water
#               -land
#               -land+water
#               -water
# note: the names of the directories have to be exactly those above,
# otherwise the script will crash since
# it cannot find the specified directory
# the script looks through all the subdirectories of the
# directory named labels and saves after each one is done

def save_tiles(name, data_base, cur):
    temp = 0
    """Save tiles to db"""
    # creating a cursor object
    # data_base = MySQLdb.connect(host="projects-db.ewi.tudelft.nl",  # host
    #                             user="pu_OkT0nkRGlc62l",  # username
    #                             passwd="TFmzM7V8ihH9",  # password
    #                             db="projects_TimeTravelMaps")  # name of the database
    # cur = database.cursor()

    for root, dirs, files in os.walk(name, topdown=False):
        # assign the label of the folder that the image is placed in

        water = 0
        land = 0
        building = 0
        if root.find("water") > -1:
            water = 1
        if root.find("land") > -1:
            land = 1
        if root.find("building") > -1:
            building = 1
        for file in files:
            # get the coordinates from the file name
            coords = file.split('_')
            y_coord = coords[0]
            x_coord = coords[1]
            year = 2016

            # sql queries
            cur.execute("INSERT INTO core_dataset "
                        + "(x_coord, y_coord, year, water, land, building) VALUES ('"
                        + str(x_coord) + "','"
                        + str(y_coord) + "','"
                        + str(year) + "','"
                        + str(water) + "','"
                        + str(land) + "','"
                        + str(building) + "');")

        # commit after each folder is done, in case something breaks
        data_base.commit()
        temp = 1
    data_base.close()

    return temp
