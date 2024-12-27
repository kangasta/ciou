from datetime import datetime
from time import sleep
from unittest import TestCase

from ciou.progress import MessageStatus, Update
from ciou.progress._message import MessageStore
from ciou.time import utcnow

class UpdateTest(TestCase):
    def test_key(self):
        self.assertEqual(Update(message="message", status=MessageStatus.SKIPPED).key, 'message')
        self.assertEqual(Update(key="key", message="message", status=MessageStatus.SKIPPED).key, 'key')


class MessageStatusTest(TestCase):
    def test_finished(self):
        status = MessageStatus.SUCCESS
        self.assertTrue(status.finished)

    def test_in_progress(self):
        status = MessageStatus.STARTED
        self.assertTrue(status.in_progress)


class MessageStoreTest(TestCase):
    def test_list_in_progress_list_finished(self):
        store = MessageStore()

        store.push(Update(message="2nd", status=MessageStatus.PENDING))
        sleep(25e-3)
        store.push(Update(message="1st", status=MessageStatus.STARTED))
        sleep(25e-3)
        store.push(Update(message="2nd", status=MessageStatus.STARTED))

        self.assertEqual(len(store.finished), 0)
        self.assertEqual(len(store.in_progress), 2)
        self.assertEqual(store.in_progress[0].message, "1st")
        self.assertEqual(store.in_progress[1].message, "2nd")

        store.push(Update(message="2nd", status=MessageStatus.SUCCESS))

        self.assertEqual(len(store.finished), 1)
        self.assertEqual(len(store.in_progress), 1)

    def test_push_updates_message(self):
        store = MessageStore()

        store.push(Update(key="test", message="Testing", status=MessageStatus.PENDING))
        sleep(25e-3)

        msg = store.in_progress[0]
        self.assertEqual(msg.message, "Testing")
        self.assertIsNone(msg.started)
        self.assertIsNone(msg.finished)

        tic = utcnow()
        sleep(25e-3)
        store.push(Update(key="test", message="Still testing", status=MessageStatus.STARTED))
        sleep(25e-3)

        self.assertEqual(msg.message, "Still testing")
        self.assertIsNone(msg.details)
        self.assertGreater(msg.started, tic)
        self.assertIsNone(msg.finished)

        toc = utcnow()
        sleep(25e-3)
        store.push(Update(key="test", message="Still testing", status=MessageStatus.ERROR, details="Test details"))

        self.assertEqual(msg.message, "Still testing")
        self.assertEqual(msg.details, "Test details")
        self.assertGreater(msg.started, tic)
        self.assertGreater(toc, msg.started)
        self.assertGreater(msg.finished, toc)

    def test_push_finished_message(self):
        store = MessageStore()

        store.push(Update(key="skipped", message="Testing skipped", status=MessageStatus.SKIPPED))
        store.push(Update(key="success", message="Testing success", status=MessageStatus.SUCCESS))
