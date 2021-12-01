import unittest

from advent_of_code.utilities import read_lines


class ReadFileLinesTest(unittest.TestCase):
    def test_read_lines(self):
        self.assertEqual(read_lines('dummy.txt'), ['This is', 'a file', 'with content', 'on multiple lines'])


if __name__ == '__main__':
    unittest.main()
