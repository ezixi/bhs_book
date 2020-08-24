from ebooklib import epub
import psycopg2
import re
import distutils.dir_util
import local_settings


class BhsBook(epub.EpubBook):
    def __init__(self, identifier, title, author, language="en"):
        book = epub.EpubBook()
        book.set_identifier(identifier)
        book.set_title(title)
        book.set_language(language)
        book.add_author(author)

        self.title = title
        self.author = author
        self.identifier = identifier
        self.language = language

    def connect_to_db(self):
        conn = psycopg2.connect(
            f"dbname={local_settings.LOCALDB} user={local_settings.LOCALUSER}"
        )
        return conn

    def get_story(self, story_id, connection):
        cur = connection.cursor()
        cur.execute(
            f"""
            SELECT post_title, post_content from wp_posts where "ID" = {story_id};
            """
        )
        data = cur.fetchall()[0]
        cur.close()
        return data

    def clean_story(self, story, replacement_rules):
        for error, replacement in replacement_rules.items():
            story = re.sub(error, replacement, story)
        return story

    def create_folder(self):
        folder_name = self.title.replace(" ", "-")
        distutils.dir_util.mkpath(f"/tmp/{folder_name}")
        return folder_name

    def write_html(self, story_name, story, chapter):
        folder_path = self.create_folder()
        path = f"/tmp/{folder_path}/{story_name}-{chapter}.html"
        with open(path, "w") as f:
            body = f"""
                <!doctype html>
                        <html lang="en">
                        <head></head>
                        <body>
                            <h1>{story_name}</h1>
                            <p>{story}</p>
                        </body>
                    </html>
            """
            f.write(body)
        return path
