import os
import sys
import unittest

from PIL import Image

sys.path.append(os.path.join(os.path.dirname("src"), '..'))
from src.scripts.tile_sorter import find_colour
from src.scripts.tile_sorter import sort_tiles


class TestTileSorter(unittest.TestCase):

    def test_simple_rgb(self):
        self.assertEqual(find_colour((255, 99, 71)), "red")
        self.assertEqual(find_colour((100, 255, 70)), "green")
        self.assertEqual(find_colour((0, 0, 255)), "blue")
        self.assertEqual(find_colour((255, 200, 10)), "yellow")
        self.assertEqual(find_colour((255, 100, 210)), "magenta")
        self.assertEqual(find_colour((150, 255, 255)), "teal")
        self.assertEqual(find_colour((255, 255, 255)), "white")
        self.assertEqual(find_colour((0, 0, 0)), "black")

    def test_invalid_rgb(self):
        self.assertEqual(find_colour((-1, -1, -1)), "part of the rgb triplet was invalid")

    def test_gray_colours(self):
        self.assertEqual(find_colour((100, 110, 110)), "gray")
        self.assertEqual(find_colour((10, 10, 10)), "gray")
        self.assertEqual(find_colour((15, 20, 10)), "gray")
        self.assertEqual(find_colour((100, 95, 105)), "gray")

    def test_sort_tiles(self):
        self.assertEqual(os.path.exists("core/test/images/building_tile.png"), True)
        self.assertEqual(os.path.exists("core/test/images/building+land_tile.png"), True)
        self.assertEqual(os.path.exists("core/test/images/building+land+water_tile.png"), True)
        self.assertEqual(os.path.exists("core/test/images/building+water_tile.png"), True)
        self.assertEqual(os.path.exists("core/test/images/land_tile.png"), True)
        self.assertEqual(os.path.exists("core/test/images/land+water_tile.png"), True)
        self.assertEqual(os.path.exists("core/test/images/water_tile.png"), True)

        im1 = Image.open("core/test/images/building_tile.png")
        im2 = Image.open("core/test/images/building+land_tile.png")
        im3 = Image.open("core/test/images/building+land+water_tile.png")
        im4 = Image.open("core/test/images/building+water_tile.png")
        im5 = Image.open("core/test/images/land_tile.png")
        im6 = Image.open("core/test/images/land+water_tile.png")
        im7 = Image.open("core/test/images/water_tile.png")

        copy1 = im1.copy()
        copy2 = im2.copy()
        copy3 = im3.copy()
        copy4 = im4.copy()
        copy5 = im5.copy()
        copy6 = im6.copy()
        copy7 = im7.copy()

        self.assertEqual(os.path.exists("core/test/labels/building/building_tile.png"), False)
        self.assertEqual(os.path.exists("core/test/labels/building+land/building+land_tile.png"), False)
        self.assertEqual(os.path.exists("core/test/labels/building+land+water/building+land+water_tile.png"), False)
        self.assertEqual(os.path.exists("core/test/labels/building+land/building+water_tile.png"), False)
        self.assertEqual(os.path.exists("core/test/labels/land/land_tile.png"), False)
        self.assertEqual(os.path.exists("core/test/labels/land+water/land+water_tile.png"), False)
        self.assertEqual(os.path.exists("core/test/labels/water/water_tile.png"), False)

        sort_tiles("core/test/images", "core/test/labels")

        self.assertEqual(os.path.exists("core/test/images/building_tile.png"), False)
        self.assertEqual(os.path.exists("core/test/images/building+land_tile.png"), False)
        self.assertEqual(os.path.exists("core/test/images/building+land+water_tile.png"), False)
        self.assertEqual(os.path.exists("core/test/images/building+water_tile.png"), False)
        self.assertEqual(os.path.exists("core/test/images/land_tile.png"), False)
        self.assertEqual(os.path.exists("core/test/images/land+water_tile.png"), False)
        self.assertEqual(os.path.exists("core/test/images/water_tile.png"), False)

        self.assertEqual(os.path.exists("core/test/labels/building/building_tile.png"), True)
        self.assertEqual(os.path.exists("core/test/labels/building+land/building+land_tile.png"), True)
        self.assertEqual(os.path.exists("core/test/labels/building+land+water/building+land+water_tile.png"), True)
        self.assertEqual(os.path.exists("core/test/labels/building+water/building+water_tile.png"), True)
        self.assertEqual(os.path.exists("core/test/labels/land/land_tile.png"), True)
        self.assertEqual(os.path.exists("core/test/labels/land+water/land+water_tile.png"), True)
        self.assertEqual(os.path.exists("core/test/labels/water/water_tile.png"), True)

        copy1.save("core/test/images/building_tile.png")
        copy2.save("core/test/images/building+land_tile.png")
        copy3.save("core/test/images/building+land+water_tile.png")
        copy4.save("core/test/images/building+water_tile.png")
        copy5.save("core/test/images/land_tile.png")
        copy6.save("core/test/images/land+water_tile.png")
        copy7.save("core/test/images/water_tile.png")

        os.remove("core/test/labels/building/building_tile.png")
        os.remove("core/test/labels/building+land/building+land_tile.png")
        os.remove("core/test/labels/building+land+water/building+land+water_tile.png")
        os.remove("core/test/labels/building+water/building+water_tile.png")
        os.remove("core/test/labels/land/land_tile.png")
        os.remove("core/test/labels/land+water/land+water_tile.png")
        os.remove("core/test/labels/water/water_tile.png")
