import unittest
import psycopg2
import html5lib
from pathlib import Path
import local_settings

from bhs_book.story import BhsStory


class StoryTest(unittest.TestCase):
    def setUp(self):
        self.replacement_rules = {
            r"<\!\-*\w*\-*\>": "",
            r"--": " — ",
            r"(?:\\+\w)+": "</p><p>",
            r"\\": "",
        }
        self.story = BhsStory(27, self.replacement_rules)
        self.conn = psycopg2.connect(
            f"dbname={local_settings.LOCALDB} user={local_settings.LOCALUSER}"
        )
        self.sample_story = self.story.get_story(self.conn)
        self.sample_html = self.story.write_html("/tmp", 1)

    def test_story_has_a_title_and_body(self):
        self.assertTrue(len(self.sample_story) == 2)

    def test_copy_is_valid_html(self):
        html5parser = html5lib.HTMLParser(strict=True)
        with open(self.sample_html, "r") as html_file:
            self.assertTrue(html5parser.parse(html_file))

    def tearDown(self):
        Path(self.story.filepath).unlink()


if __name__ == "__main__":
    unittest.main()
