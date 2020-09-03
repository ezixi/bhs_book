from ebooklib import epub
from ebooklib.utils import create_pagebreak
import psycopg2
import re


class BhsStory:
    def __init__(self, story_id, replacement_rules, connection):
        self.story_id = story_id
        self.replacement_rules = replacement_rules
        self.connection = connection
        self.title, self.story = self.get_story()
        self.story = self.clean_story()
        self.html = self.write_html()

    def get_story(self):
        cur = self.connection.cursor()
        cur.execute(
            f"""
            SELECT post_title, post_content from wp_posts where "ID" = {self.story_id};
            """
        )
        data = cur.fetchall()[0]
        cur.close()
        return data[0], data[1]

    def clean_story(self):
        for error, replacement in self.replacement_rules.items():
            self.story = re.sub(error, replacement, self.story)
        return self.story

    def write_html(self):
        html = f"""
            <!doctype html>
                    <html lang="en">
                    <head></head>
                    <body>
                        <h1>{self.title}</h1>
                        <p>{self.story}</p>
                    </body>
                </html>
        """
        return html

    def create_chapter(self, order):
        filename = self.title.replace(" ", "-")
        filepath = f"{filename}-{order}.xhtml"
        chapter = epub.EpubHtml(title=self.title, file_name=filepath, lang="en")
        chapter.content = self.html
        chapter.content += create_pagebreak("blah")
        return chapter
