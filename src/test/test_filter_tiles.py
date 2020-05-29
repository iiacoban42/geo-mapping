import os
import sys
import unittest
from PIL import Image

sys.path.append(os.path.join(os.path.dirname("src"), '..'))
from src.scripts.filter_tiles import delete_img
from src.scripts.filter_tiles import cleanup


class TestFilterTiles(unittest.TestCase):

    def test_delete_img_valid_black_tile(self):
        im1 = Image.open("test/black_tile.png")
        im2 = im1.copy()
        im2.save("test/black_tile_copy.png")
        self.assertEqual(os.path.exists("test/black_tile_copy.png"), True)
        self.assertEqual("successfully removed", delete_img("test/black_tile_copy.png", "test/black_tile.png"))
        self.assertEqual(os.path.exists("test/black_tile_copy.png"), False)

    def test_delete_img_non_png_file(self):
        self.assertEqual(os.path.exists("test/not_a_png"), True)
        self.assertEqual("file is not a valid png", delete_img("test/not_a_png", "test/black_tile.png"))
        self.assertEqual(os.path.exists("test/not_a_png"), True)

    def test_delete_img_invalid_png_file(self):
        self.assertEqual(os.path.exists("test/not_a_valid_png.png"), True)
        self.assertEqual("file is not a valid png", delete_img("test/not_a_valid_png.png", "test/black_tile.png"))
        self.assertEqual(os.path.exists("test/not_a_valid_png.png"), True)

    def test_delete_img_inexistent_file(self):
        self.assertEqual(os.path.exists("test/not_a_file.png"), False)
        self.assertEqual("file does not exist", delete_img("test/not_a_file.png", "test/black_tile.png"))
        self.assertEqual(os.path.exists("test/not_a_file.png"), False)

    def test_delete_img_valid_coloured_time(self):
        self.assertEqual(os.path.exists("test/sample_tile.png"), True)
        self.assertEqual("image was not black", delete_img("test/sample_tile.png", "test/black_tile.png"))
        self.assertEqual(os.path.exists("test/sample_tile.png"), True)

    def test_cleanup_delete_black(self):
        im1 = Image.open("test/black_tile.png")
        im2 = im1.copy()
        im2.save("test/dir_to_cleanup/black1.png")
        im2.save("test/dir_to_cleanup/black2.png")
        im2.save("test/dir_to_cleanup/black3.png")
        self.assertEqual(os.path.exists("test/dir_to_cleanup/black1.png"), True)
        self.assertEqual(os.path.exists("test/dir_to_cleanup/black2.png"), True)
        self.assertEqual(os.path.exists("test/dir_to_cleanup/black3.png"), True)
        cleanup("test/dir_to_cleanup", "test/black_tile.png")
        self.assertEqual(os.path.exists("test/dir_to_cleanup/black1.png"), False)
        self.assertEqual(os.path.exists("test/dir_to_cleanup/black2.png"), False)
        self.assertEqual(os.path.exists("test/dir_to_cleanup/black3.png"), False)

    def test_cleanup_not_delete_coloured(self):
        self.assertEqual(os.path.exists("test/dir_to_cleanup/coloured1.png"), True)
        self.assertEqual(os.path.exists("test/dir_to_cleanup/coloured2.png"), True)
        self.assertEqual(os.path.exists("test/dir_to_cleanup/coloured3.png"), True)
        cleanup("test/dir_to_cleanup", "test/black_tile.png")
        self.assertEqual(os.path.exists("test/dir_to_cleanup/coloured1.png"), True)
        self.assertEqual(os.path.exists("test/dir_to_cleanup/coloured2.png"), True)
        self.assertEqual(os.path.exists("test/dir_to_cleanup/coloured3.png"), True)
