from ebooklib import epub
import psycopg2
import re


class BhsStory:
    def __init__(self, story_id, replacement_rules):
        self.story_id = story_id
        self.replacement_rules = replacement_rules

    def get_story(self):
        connection = self.connect_to_db()
        cur = connection.cursor()
        cur.execute(
            f"""
            SELECT post_title, post_content from wp_posts where "ID" = {self.story_id};
            """
        )
        data = cur.fetchall()[0]
        cur.close()
        return data

    def clean_story(self, story):
        for error, replacement in self.replacement_rules.items():
            self.story = re.sub(error, replacement, self.story)
        return self.story

    def write_html(self, path, title, story, chapter):
        filename = f"{path}/{title}-{chapter}.html"
        with open(filename, "w") as f:
            body = f"""
                <!doctype html>
                        <html lang="en">
                        <head></head>
                        <body>
                            <h1>{title}</h1>
                            <p>{story}</p>
                        </body>
                    </html>
            """
            f.write(body)
        return filename
