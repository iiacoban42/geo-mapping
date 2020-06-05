import os
import sys
import unittest
import urllib.request
from urllib import request

from PIL import Image

sys.path.append(os.path.join(os.path.dirname("src"), '..'))
from src.scripts.improved_tile_retriever import check_full_white
from src.scripts.improved_tile_retriever import check_transparent
from src.scripts.improved_tile_retriever import save_tile
from src.scripts.improved_tile_retriever import save_all_tiles
from src.scripts.improved_tile_retriever import check_request
from src.scripts.improved_tile_retriever import finish_request

from core.models import UsableTiles as UsableTilesTable

from unittest.mock import patch, MagicMock


# pylint: disable=all

class TestImprovedTileRetriever(unittest.TestCase):

    def test_half_transparent_half_colour(self):
        im = Image.open("core/test/improved_tile_retriever_test_images/half_transparent_half_colour.png", 'r')
        pix_val = list(im.getdata())
        self.assertEqual(check_transparent(pix_val), True)

    def test_half_transparent_half_white(self):
        im = Image.open("core/test/improved_tile_retriever_test_images/half_transparent_half_white.png", 'r')
        pix_val = list(im.getdata())
        self.assertEqual(check_transparent(pix_val), True)
        self.assertEqual(check_full_white(pix_val), False)

    def test_half_white_half_colour(self):
        im = Image.open("core/test/improved_tile_retriever_test_images/half_white_half_colour.png", 'r')
        pix_val = list(im.getdata())
        self.assertEqual(check_transparent(pix_val), False)
        self.assertEqual(check_full_white(pix_val), False)

    def test_save_all_invalid_url(self):
        self.assertEqual(save_all_tiles(1, range(1, 2), range(1, 2)), "success")

    def test_finish_request(self):
        im1 = Image.open("core/test/improved_tile_retriever_test_images/full_transparent.png", 'r')
        pix_val1 = list(im1.getdata())
        self.assertEqual(check_transparent(pix_val1), True)
        finish_request(im1, 1, 1, 1)
        tiles1 = UsableTilesTable.objects.all().count()
        self.assertEqual(tiles1, 0)

        im2 = Image.open("core/test/improved_tile_retriever_test_images/full_white.png", 'r')
        pix_val2 = list(im2.getdata())
        self.assertEqual(check_transparent(pix_val2), False)
        self.assertEqual(check_full_white(pix_val2), True)
        finish_request(im2, 1, 1, 1)
        tiles2 = UsableTilesTable.objects.all().count()
        self.assertEqual(tiles2, 0)

        im3 = Image.open("core/test/improved_tile_retriever_test_images/half_white_half_colour.png", 'r')
        finish_request(im3, 1, 1, 1)
        tiles3 = UsableTilesTable.objects.all().count()
        self.assertEqual(tiles3, 1)

    def test_check_request(self):

        check_request("1", 1, 1, 1)

        real = urllib.request
        real.urlopen = MagicMock(name='urlopen')
        real.urlopen.return_value = "core/test/improved_tile_retriever_test_images/full_transparent.png"

        check_request("1", 1, 1, 1)

        real.urlopen.assert_called_once_with("1")
