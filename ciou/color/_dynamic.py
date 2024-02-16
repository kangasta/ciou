import sys

from ._color import _build_colors


class _Dynamic:
    def __init__(self):
        for name, value in _build_colors().items():
            setattr(self, name, value)


sys.modules[__name__] = _Dynamic()
