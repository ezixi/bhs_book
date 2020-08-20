import unittest
import bhs_book
import psycopg2
import local_settings


class BookTest(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(
            f"dbname={local_settings.LOCALDB} user={local_settings.LOCALUSER}"
        )

    def test_story_ids_exist(self):
        self.assertTrue(len(bhs_book.get_story_ids()) > 0)

    def test_story_has_a_title_and_body(self):
        self.assertTrue(len(bhs_book.get_story(27, self.conn)) == 2)


if __name__ == "__main__":
    unittest.main()
