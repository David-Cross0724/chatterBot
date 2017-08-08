from unittest import TestCase
from chatterbot import queues


class FixedSizeQueueTests(TestCase):

    def setUp(self):
        self.queue = queues.FixedSizeQueue(maxsize=2)

    def test_append(self):
        self.queue.append(0)
        self.assertIn(0, self.queue)

    def test_contains(self):
        self.queue.queue.append(0)
        self.assertIn(0, self.queue)

    def test_empty(self):
        self.assertTrue(self.queue.empty())

    def test_not_empty(self):
        self.queue.append(0)
        self.assertFalse(self.queue.empty())

    def test_maxsize(self):
        self.queue.append(0)
        self.queue.append(1)
        self.queue.append(2)

        self.assertNotIn(0, self.queue)
        self.assertIn(1, self.queue)
        self.assertIn(2, self.queue)

    def test_peek_empty_queue(self):
        self.assertIsNone(self.queue.peek())

    def test_peek(self):
        self.queue.append(4)
        self.queue.append(5)
        self.queue.append(6)

        self.assertEqual(self.queue.peek(), 6)
