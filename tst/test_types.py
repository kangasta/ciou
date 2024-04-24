from freezegun import freeze_time
import os
from queue import Queue
from time import sleep
from unittest import TestCase

from ciou.types import ensure_list


class TypesTest(TestCase):
    def test_ensure_list(self):
        for name, value, expected in [
            ('None', None, []),
            ('str', "value", ["value"]),
            ('generator', (f'i{i}' for i in range(1,4)), ["i1", "i2", "i3"]),
            ('list', [1,2,3], [1,2,3]),
        ]:
            with self.subTest(name):
                self.assertEqual(ensure_list(value), expected)
