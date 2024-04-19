import random
from unittest import TestCase
from uuid import uuid4

from ciou.snapshot import snapshot, REPLACE_DURATION, REPLACE_TIMESTAMP, REPLACE_UUID
from ciou.time import timestamp


class SnapshotTest(TestCase):
    maxDiff = None

    def test_replace_single(self):
        content = f'''
real    0m{random.uniform(0,1):.3f}s
user    0m{random.uniform(0,1):.3f}s
sys     0m{random.uniform(0,1):.3f}s'''

        self.assertEqual(*snapshot('test_replace_single', content, replace=(r'[0-9]\.[0-9]+', '<DURATION>')))

    def test_replace_many(self):
        content = f'id: {uuid4()}, started: {timestamp()}, duration: {random.uniform(0,1):.3f} ms'
        replaces = [
            REPLACE_TIMESTAMP,
            REPLACE_DURATION,
            REPLACE_UUID,
        ]

        self.assertEqual(*snapshot('test_replace_many', content, replace=replaces))
