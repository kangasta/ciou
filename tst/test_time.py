from datetime import datetime, timedelta, timezone

from freezegun import freeze_time
from queue import Queue
from time import sleep
from unittest import TestCase

from ciou.time import timestamp, Ticker


ARGS = (2024, 2, 20, 2, 20, 24, 1)
TIMESTAMP = '2024-02-20T02:20:24.000001Z'


class TimeTest(TestCase):
    maxDiff = None

    @freeze_time(TIMESTAMP)
    def test_timestamp(self):
        self.assertEqual(timestamp(), TIMESTAMP)

    @freeze_time(TIMESTAMP, auto_tick_seconds=0.050)
    def test_ticker(self):
        ticks = Queue()
        ticker = Ticker(0.050, ticks)
        ticker.start()

        sleep(0.175)
        ticker.stop()

        self.assertEqual(ticks.get(), '2024-02-20T02:20:24.000001Z')
        self.assertEqual(ticks.get(), '2024-02-20T02:20:24.050001Z')
        self.assertEqual(ticks.get(), '2024-02-20T02:20:24.100001Z')


class TimestampTest(TestCase):
    def test_non_aware(self):
        with self.assertRaises(ValueError):
            timestamp(datetime(*ARGS))

    def test_non_utc(self):
        with self.assertRaises(ValueError):
            timestamp(datetime(*ARGS, tzinfo=timezone(timedelta(hours=3), "EEST")))

    def test_utc(self):
        self.assertEqual(timestamp(datetime(*ARGS, tzinfo=timezone(timedelta(), "GMT"))), TIMESTAMP)
