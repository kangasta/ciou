import os
from unittest import TestCase

from ciou.color import bold, colors, fg_red, fg_green, no_color, color_palette, len_without_ansi_escapes

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
        self.assertEqual(color_palette() + "\n", COLOR_PALETTE)

    def test_no_color(self):
        self.assertEqual(no_color("input"), "input")

    def test_len_without_ansi_escapes(self):
        bold_green = colors(bold, fg_green)
        self.assertEqual(len_without_ansi_escapes(fg_red("red")), 3)
        self.assertEqual(len_without_ansi_escapes(bold_green("bold_green")), 10)
        self.assertEqual(len_without_ansi_escapes("\033[31;1;4mHello\033[0m"), 5)
        self.assertEqual(len_without_ansi_escapes("str_with_no_escapes"), 19)
