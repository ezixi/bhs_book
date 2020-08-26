import unittest
from pathlib import Path
from bhs_book.book import BhsBook


class BookTest(unittest.TestCase):
    def setUp(self):
        self.book = BhsBook("identifier", "title", "author")

    def test_folder_exists(self):
        self.assertTrue(Path(self.book.path).exists())

    def tearDown(self):
        Path(self.book.path).rmdir()


if __name__ == "__main__":
    unittest.main()
