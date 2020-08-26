import unittest
from pathlib import Path
from bhs_book.book import BhsBook


class BookTest(unittest.TestCase):
    def setUp(self):
        self.book = BhsBook("identifier", "title", "author")
        self.book_folder = self.book.create_folder()

    def test_folder_exists(self):
        self.assertTrue(Path(self.book_folder).exists())

    def tearDown(self):
        Path(self.book_folder).rmdir()


if __name__ == "__main__":
    unittest.main()
