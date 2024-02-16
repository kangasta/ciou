from datetime import datetime, timedelta
from io import StringIO
from unittest import TestCase

from ciou.progress import MessageStatus, Message, OutputConfig

DETAILS_WITH_NEWLINES = '''Output:

+ echo 'Details with newlines are assumed to be preformatted. Thus, newline characters should not be replaced with other whitespace when wrapping the text.'
Details with newlines are assumed to be preformatted. Thus, newline characters should not be replaced with other whitespace when wrapping the text.
+ cat not-found
cat: not-found: No such file or directory'''
EXPECTED_STARTED = "\x1b[34m> \x1b[0mTesting                                                                                     \x1b[90m  10 s\x1b[0m\n"
EXPECTED_WITH_DETAILS = '''\x1b[32m✓ \x1b[0m\x1b[32mTesting                                                                                     \x1b[0m\x1b[90m 123 s\x1b[0m
  Output:

  + echo 'Details with newlines are assumed to be preformatted. Thus, newline characters should not
  be replaced with other whitespace when wrapping the text.'
  Details with newlines are assumed to be preformatted. Thus, newline characters should not be
  replaced with other whitespace when wrapping the text.
  + cat not-found
  cat: not-found: No such file or directory
'''

class OutputConfigTest(TestCase):
    maxDiff = None

    def test_get_message_text(self):
        testdata = [
            (
                OutputConfig(target=StringIO()),
                Message(key="test", message="Testing", status=MessageStatus.STARTED, started=datetime.utcnow() - timedelta(seconds=10)),
                EXPECTED_STARTED,
            ),
            (
                OutputConfig(color_message=True, target=StringIO()),
                Message(key="test", message="Testing", details=DETAILS_WITH_NEWLINES, status=MessageStatus.SUCCESS, started=datetime.utcnow() - timedelta(seconds=123), finished=datetime.utcnow()),
                EXPECTED_WITH_DETAILS,
            ),
        ]

        for config, message, expected in testdata:
            self.assertEqual(config.get_message_text(message, 1), expected)
