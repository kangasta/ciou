import io
import platform
import sys
from unittest import TestCase

from ciou.terminal import is_windows_terminal

class TerminalTest(TestCase):
    def test_is_windows_terminal(self):
        if platform.system() != "Windows":
            self.assertFalse(is_windows_terminal(sys.stderr))

        if platform.system() == "Windows":
            self.assertEqual(is_windows_terminal(sys.stderr), sys.stderr.isatty())
            self.assertFalse(is_windows_terminal(io.StringIO()))
