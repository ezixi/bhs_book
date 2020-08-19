import unittest
import bhs_book


class BookTest(unittest.TestCase):
    def test_story_ids_exist(self):
        self.assertTrue(len(bhs_book.get_story_ids()) > 0)


if __name__ == "__main__":
    unittest.main()
