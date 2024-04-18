from io import StringIO
from unittest import TestCase, main

from ciou.snapshot import rewind_and_read, snapshot

class SnapshotTest(TestCase):
    maxDiff = None

    def test_snapshot(self):
        target = StringIO()
        print("Output to validate with `snapshot`.", file=target)

        actual = rewind_and_read(target)
        self.assertEqual(actual, snapshot("test_snapshot", actual))

        print("New line that is not present in the snapshot.", file=target)

        actual = rewind_and_read(target)
        self.assertNotEqual(actual, snapshot("test_snapshot", actual))

if __name__ == "__main__":
    main()
