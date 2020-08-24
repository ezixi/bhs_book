from ebooklib import epub
import psycopg2
import re
import distutils.dir_util
import local_settings


class BhsStory:
    def __init__(self, story_id, title, body, replacement_rules):
        self.story_id = story_id
        self.title = title
        self.body = body
        self.replacement_rules = replacement_rules

    def connect_to_db(self):
        conn = psycopg2.connect(
            f"dbname={local_settings.LOCALDB} user={local_settings.LOCALUSER}"
        )
        return conn

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

    def clean_story(self):
        for error, replacement in self.replacement_rules.items():
            self.story = re.sub(error, replacement, self.story)
        return self.story
