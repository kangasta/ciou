import os
import yaml

from jinja2.exceptions import UndefinedError

from unittest import TestCase

from ciou.color import bold, colors, fg_red, fg_green, _color_palette

TST_DIR = os.path.dirname(os.path.realpath(__file__))
with open(f'{TST_DIR}/color_palette.txt', 'r') as f:
    COLOR_PALETTE = f.read()

class ColorTest(TestCase):
    maxDiff = None

    def test_fg_red(self):
        self.assertEqual(fg_red("input"), '\033[31minput\033[0m')
        self.assertEqual(fg_red("red") + "default", '\033[31mred\033[0mdefault')

    def test_colors(self):
        bold_green = colors(bold, fg_green)
        self.assertEqual(bold_green("input"), '\033[32m\033[1minput\033[0m')
        self.assertEqual(bold_green("bold_green") + "default", '\033[32m\033[1mbold_green\033[0mdefault')

    def test_color_palette(self):
        self.assertEqual(_color_palette() + "\n", COLOR_PALETTE)