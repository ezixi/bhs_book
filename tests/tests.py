import unittest
import bhs_book


class BookTest(unittest.TestCase):
    def test_id_is_an_integer(self):
        self.assertTrue(isinstance(bhs_book.get_story_ids(), int))


if __name__ == "__main__":
    unittest.main()
