import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname("src"), '..'))
from src.scripts.colour_detector import extract_colours


class TestColourDetector(unittest.TestCase):

    def test_valid_tile(self):
        expected_result = [((255, 255, 255), 48.25),
                           ((255, 79, 82), 17.25),
                           ((79, 255, 104), 17.25),
                           ((79, 81, 255), 17.25)]
        self.assertEqual(extract_colours("core/test/sample_tile.png"), expected_result)

    def test_inexistent_tile(self):
        expected_result = []
        self.assertEqual(extract_colours("test/inexistent_tile.png"), expected_result)
