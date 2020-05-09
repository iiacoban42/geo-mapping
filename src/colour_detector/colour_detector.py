import webcolors
from colorthief import ColorThief


def get_colour_name(rgb_triplet):
    min_colours = {}
    for key, name in webcolors.HTML4_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - rgb_triplet[0]) ** 2
        gd = (g_c - rgb_triplet[1]) ** 2
        bd = (b_c - rgb_triplet[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


color_thief = ColorThief('tile.jpg')
# get the dominant color
dominant_color = color_thief.get_color(quality=1)
palette = color_thief.get_palette(color_count=30, quality=1)  # 30 can be adjusted

print(dominant_color, get_colour_name(dominant_color))
for el in palette:
    print(el, get_colour_name(el))
