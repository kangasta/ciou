from datetime import datetime, timedelta
from io import StringIO
from unittest import TestCase

from ciou.progress import MessageStatus, Message, OutputConfig

from tst.snapshot import snapshot, rewind_and_read

DETAILS_WITH_NEWLINES = '''Output:

+ echo 'Details with newlines are assumed to be preformatted. Thus, newline characters should not be replaced with other whitespace when wrapping the text.'
Details with newlines are assumed to be preformatted. Thus, newline characters should not be replaced with other whitespace when wrapping the text.
+ cat not-found
cat: not-found: No such file or directory'''
LONG_MESSAGE = '''The  message  should be truncated to fit a single row.
\tAll whitespace characters are replaced with spaces.
'''

class OutputConfigTest(TestCase):
    maxDiff = None

    def test_get_message_text(self):
        testdata = [
            (
                'started',
                OutputConfig(target=StringIO()),
                Message(key="test", message="Testing", status=MessageStatus.STARTED, started=datetime.utcnow() - timedelta(seconds=10)),
            ),
            (
                'started',
                OutputConfig(target=StringIO()),
                Message(key="test", message="Testing", status=MessageStatus.STARTED, started=datetime.utcnow() - timedelta(seconds=10), details=DETAILS_WITH_NEWLINES),
            ),
            (
                'long_message',
                OutputConfig(target=StringIO()),
                Message(key="test", message=LONG_MESSAGE, status=MessageStatus.WARNING, started=datetime.utcnow() - timedelta(seconds=10)),
            ),
            (
                'with_details',
                OutputConfig(color_message=True, target=StringIO()),
                Message(key="test", message="Testing", details=DETAILS_WITH_NEWLINES, status=MessageStatus.SUCCESS, started=datetime.utcnow() - timedelta(seconds=123), finished=datetime.utcnow()),
            ),
        ]

        for test, config, message in testdata:
            with self.subTest(test):
                actual = config.get_message_text(message, 1)
                expected = snapshot(__file__, f'test_get_message_text_{test}', config.get_message_text(message, 1))

                self.assertEqual(actual, expected)
