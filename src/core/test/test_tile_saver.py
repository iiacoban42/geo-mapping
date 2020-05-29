import unittest

from mock import patch

from src.scripts.tile_saver import save_tiles


class TestTileSaver(unittest.TestCase):
    def test_tile_saver(self):
        with patch('django.db.connections') as database:
            mock_cursor = database.db.cursor()
            self.assertEqual(save_tiles('core/test/labels_test', database, mock_cursor), 1)
            mock_cursor.execute.assert_called_once_with("INSERT INTO core_dataset "
                                                        + "(x_coord, y_coord, year, water, land, building) VALUES ('"
                                                        + str(1) + "','"
                                                        + str(1) + "','"
                                                        + str(2016) + "','"
                                                        + str(1) + "','"
                                                        + str(1) + "','"
                                                        + str(1) + "');")

