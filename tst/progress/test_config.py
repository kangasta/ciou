from datetime import timedelta
from io import StringIO
from unittest import TestCase

from ciou.color import fg_green
from ciou.progress import MessageStatus, Message, OutputConfig
from ciou.progress._renderer import MessageRenderer
from ciou.snapshot import snapshot
from ciou.time import utcnow

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

    def test_get_status_color(self):
        c = OutputConfig()
        color = c.get_status_color(MessageStatus.SUCCESS)
        self.assertEqual(fg_green('text'), color('text'))

        c = OutputConfig(disable_colors=True)
        color = c.get_status_color(MessageStatus.SUCCESS)
        self.assertEqual('text', color('text'))

    def test_get_message_text(self):
        testdata = [
            (
                'started',
                OutputConfig(target=StringIO()),
                Message(key="test", message="Testing", status=MessageStatus.STARTED, started=utcnow() - timedelta(seconds=10)),
            ),
            (
                'started',
                OutputConfig(target=StringIO()),
                Message(key="test", message="Testing", status=MessageStatus.STARTED, started=utcnow() - timedelta(seconds=10), details=DETAILS_WITH_NEWLINES),
            ),
            (
                'long_message',
                OutputConfig(target=StringIO()),
                Message(key="test", message=LONG_MESSAGE, status=MessageStatus.WARNING, started=utcnow() - timedelta(seconds=10)),
            ),
            (
                'with_details',
                OutputConfig(color_message=True, target=StringIO()),
                Message(key="test", message="Testing", details=DETAILS_WITH_NEWLINES, status=MessageStatus.SUCCESS, started=utcnow() - timedelta(seconds=123), finished=utcnow()),
            ),
        ]

        for test, config, message in testdata:
            with self.subTest(test):
                renderer = MessageRenderer(config)
                actual = renderer.render_message(message)
                self.assertEqual(
                    *snapshot(f'test_get_message_text_{test}', actual))
