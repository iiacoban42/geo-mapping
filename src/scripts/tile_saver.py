"""Module for saving labeled tiles to the database"""
import os
import MySQLdb


# usage: place your "labels" folder in the same folder as this script
#        labels has subdirectories with all possible combinations of labels:
#               -building
#               -building+land
#               -building+land+water
#               -building+water
#               -land
#               -land+water
#               -water
# note: the names of the directories have to be exactly those above, otherwise the script will crash since
# it cannot find the specified directory
# the script looks through all the subdirectories of the directory named labels and saves after each one is done


def save_tiles():
    db = MySQLdb.connect(host="projects-db.ewi.tudelft.nl",  # host
                         user="pu_OkT0nkRGlc62l",  # username
                         passwd="TFmzM7V8ihH9",  # password
                         db="projects_TimeTravelMaps")  # name of the database

    # creating a cursor object
    cur = db.cursor()

    for root, dirs, files in os.walk("labels", topdown=False):
        # assign the label of the folder that the image is placed in
        water = 0
        land = 0
        building = 0
        if root.__contains__("water"):
            water = 1
        if root.__contains__("land"):
            land = 1
        if root.__contains__("building"):
            building = 1

        for file in files:
            # get the coordinates from the file name
            coords = file.split('_')
            y_coord = coords[0]
            x_coord = coords[1]
            year = 2016

            # sql queries
            cur.execute("INSERT INTO core_dataset (x_coord, y_coord, year, water, land, building) VALUES (\'"
                        + str(x_coord) + "\',\'"
                        + str(y_coord) + "\',\'"
                        + str(year) + "\',\'"
                        + str(water) + "\',\'"
                        + str(land) + "\',\'"
                        + str(building) + "\');")

        # commit after each folder is done, in case something breaks
        db.commit()

    db.close()


from datetime import datetime

start = datetime.now()

save_tiles()

# calculate running time, just for the sake of it
print(datetime.now() - start)
