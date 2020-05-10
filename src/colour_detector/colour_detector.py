"""Module for extracting colors from the tiles"""
import extcolors


def extract_colors():
    """Run extcolors on the input image (now it runs on tile.jpg to exemplify behavior)"""
    colors, pixel_count = extcolors.extract("tile.jpg")
    extcolors.print_result(colors, pixel_count)
