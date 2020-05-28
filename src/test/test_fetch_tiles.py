import os
import sys
import unittest
import urllib
from PIL import Image

sys.path.append(os.path.join(os.path.dirname("src"), '..'))
from src.scripts.fetch_tiles import get_map


class TestFetchTiles(unittest.TestCase):

    def test_get_one_tile(self):
        """This test case retrieves one valid tile from the tile server"""
        get_map(2016, range(75077, 75078), range(74956, 74957), "test")
        self.assertEqual(os.path.exists("74956_75077.png"), True)
        img1 = Image.open("74956_75077.png")
        img1.verify()
        os.remove("74956_75077.png")

    def test_get_more_tiles(self):
        """This test case retrieves two valid tiles from the tile server"""
        get_map(2016, range(75078, 75080), range(74956, 74957), "test")
        self.assertEqual(os.path.exists("74956_75078.png"), True)
        self.assertEqual(os.path.exists("74956_75079.png"), True)
        img1 = Image.open("74956_75078.png")
        img2 = Image.open("74956_75079.png")
        img1.verify()
        img2.verify()
        os.remove("74956_75078.png")
        os.remove("74956_75079.png")

    def test_inexistent_tile(self):
        """This test case tries to access a tile that does not exist on the tile server"""
        self.assertRaises(urllib.error.HTTPError, get_map, 2016, range(75000, 75001), range(74956, 74957), "test")

    def test_invalid_folder(self):
        """This test case tries to place the retrieved tile in an invalid folder"""
        self.assertRaises(FileNotFoundError, get_map, 2016, range(75078, 75080), range(74956, 74957), "inexistent_folder")

    def test_inexistent_year(self):
        """This test case tries to access a tile from a year that does not exist on the tile server"""
        get_map(1, range(1, 2), range(1, 2), "test")
        # the image is indeed retrieved, but the file cannot be opened because it is corrupted
        self.assertRaises(OSError, Image.open, "74956_75078.png")
        os.remove("1_1.png")
