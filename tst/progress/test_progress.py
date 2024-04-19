from io import StringIO
from unittest import TestCase

from ciou.progress import OutputConfig, Progress
from ciou.snapshot import snapshot, rewind_and_read

def noop():
    pass

def warn():
    raise RuntimeWarning("Warning message")

def err():
    raise RuntimeError("Error message")

class ProgressTest(TestCase):
    maxDiff = None

    def test_context_manager(self):
        tests = [
            ("success", noop,),
            ("warning", warn,),
            ("error", err,),
        ]

        for status, function in tests:
            with self.subTest(status):
                target = StringIO()
                p = Progress(OutputConfig(target=target))
                p.start()

                with p.task(f"Test progress task contextmanager {status}"):
                    function()

                p.stop()
                actual = rewind_and_read(target)
                self.assertEqual(*snapshot(f'test_context_manager_{status}', actual))
