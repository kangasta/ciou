from unittest import TestCase

from ciou.snapshot import json_snapshot, REPLACE_TIMESTAMP
from ciou.streams import run
from ciou.streams._run import _parse_command


SCRIPT = """
echo "Counting to 10"
for i in $(seq 1 10); do
  echo "$i"
done
"""


class RunTest(TestCase):
    def test_parse_command(self):
        self.assertEqual(_parse_command(("echo", "Hello, world!")), ["echo", "Hello, world!"])
        self.assertEqual(_parse_command('echo "Hello, world!"'), ["echo", "Hello, world!"])
        self.assertEqual(_parse_command(SCRIPT), ["sh", "-ec", SCRIPT])

    def test_run_hello_world(self):
        res = run(("echo", "Hello, world!",))

        self.assertTrue(res.success)
        self.assertEqual(*json_snapshot('test_streams_run_hello_world', res.console.to_serializable(), replace=REPLACE_TIMESTAMP))

    def test_run_script(self):
        res = run(SCRIPT)

        self.assertTrue(res.success)
        self.assertEqual(*json_snapshot('test_streams_run_script', res.console.to_serializable(), replace=REPLACE_TIMESTAMP))
