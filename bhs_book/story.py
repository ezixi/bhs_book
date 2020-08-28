from ebooklib import epub
import psycopg2
import re


class BhsStory:
    def __init__(self, story_id, replacement_rules):
        self.story_id = story_id
        self.replacement_rules = replacement_rules

    def get_story(self, connection):
        cur = connection.cursor()
        cur.execute(
            f"""
            SELECT post_title, post_content from wp_posts where "ID" = {self.story_id};
            """
        )
        data = cur.fetchall()[0]
        cur.close()
        self.title = data[0]
        self.story = data[1]
        return self.title, self.story

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
        self.html = html
        return html

    def create_chapter(self, order):
        filename = self.title.replace(" ", "-")
        filepath = f"{filename}-{order}.xhtml"
        chapter = epub.EpubHtml(title=self.title, file_name=filepath, lang="en")
        chapter.content = self.html
        return chapter
