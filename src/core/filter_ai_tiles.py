"""Module that filters a set of tiles based on a specific label"""

# pylint: disable=[import-error, no-name-in-module]

from core.models import AI_Characteristics as AICharsTable


def get_land(tiles):
    """Filters by land"""
    tile_list = []
    for tile in tiles:
        res = AICharsTable.objects.filter(tiles_id=tile)
        if len(res) > 0 and res[0].land_prediction == 1:
            tile_list.append(res[0])
    return tile_list


def get_water(tiles):
    """Filters by water"""
    tile_list = []
    for tile in tiles:
        res = AICharsTable.objects.filter(tiles_id=tile)
        if len(res) > 0 and res[0].water_prediction == 1:
            tile_list.append(res[0])
    return tile_list


def get_building(tiles):
    """Filters by buildings"""
    tile_list = []
    for tile in tiles:
        res = AICharsTable.objects.filter(tiles_id=tile)
        if len(res) > 0 and res[0].buildings_prediction == 1:
            tile_list.append(res[0])
    return tile_list


def get_tiles_with_label(label, tiles):
    """Filter by label"""
    tile_list = []
    if label == 'water':
        tile_list = get_water(tiles)
    elif label == 'land':
        tile_list = get_land(tiles)
    elif label == 'building':
        tile_list = get_building(tiles)
    return tile_list
