import unittest

from src.scripts.colour_detector import extract_colors


class TestStringMethods(unittest.TestCase):

    def test_valid_tile(self):
        expected_result = [((255, 255, 255), 48.25),
                           ((255, 79, 82), 17.25),
                           ((79, 255, 104), 17.25),
                           ((79, 81, 255), 17.25)]
        self.assertEqual(extract_colors("sample_tile.png"), expected_result)

    def test_inexistent_tile(self):
        expected_result = []
        self.assertEqual(extract_colors("inexistent_tile.png"), expected_result)