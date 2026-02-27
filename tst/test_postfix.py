from unittest import TestCase

from ciou.string import with_random_postfix


class PostfixTest(TestCase):
    def test_random_postfix(self):
        value = "test"
        a = with_random_postfix(value)
        self.assertTrue(a.startswith(value))
        self.assertEqual(len(a), len(value) + 6)  # 1 for '-' and 5 for random chars

        b = with_random_postfix(value)
        self.assertTrue(b.startswith(value))
        self.assertEqual(len(b), len(value) + 6)

        self.assertNotEqual(a, b)  # Ensure different postfixes are generated

    def test_random_postfix_separator(self):
        value = "test"
        a = with_random_postfix(value, separator='_')
        self.assertTrue(a.startswith(value))
        self.assertEqual(len(a), len(value) + 6)  # 1 for '_' and 5 for random chars
        self.assertIn('_', a)  # Ensure the separator is included

        b = with_random_postfix(value, separator='')
        self.assertTrue(b.startswith(value))
        self.assertEqual(len(b), len(value) + 5)
        self.assertNotIn('-', b)  # Ensure no separator is included
