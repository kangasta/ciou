from freezegun import freeze_time
import os
from queue import Queue
from time import sleep
from unittest import TestCase

from ciou.time import timestamp, Ticker


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
