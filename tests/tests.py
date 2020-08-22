import unittest
import psycopg2
import html5lib
import local_settings

from bhs_book import BhsBook


class BookTest(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(
            f"dbname={local_settings.LOCALDB} user={local_settings.LOCALUSER}"
        )
        self.sample_story = BhsBook.get_story(self, 27, self.conn)
        self.sample_html = BhsBook.write_html(
            self, self.sample_story[0], self.sample_story[1]
        )

    def test_story_has_a_title_and_body(self):
        self.assertTrue(len(self.sample_story) == 2)

    def test_copy_is_valid_html(self):
        html5parser = html5lib.HTMLParser(strict=True)
        self.assertTrue(html5parser.parse(self.sample_html))


if __name__ == "__main__":
    unittest.main()
