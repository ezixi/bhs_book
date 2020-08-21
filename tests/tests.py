import unittest
import psycopg2
import local_settings

from bhs_book import BhsBook


class BookTest(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(
            f"dbname={local_settings.LOCALDB} user={local_settings.LOCALUSER}"
        )

    def test_story_has_a_title_and_body(self):
        self.assertTrue(len(BhsBook.get_story(self, 27, self.conn)) == 2)


if __name__ == "__main__":
    unittest.main()
