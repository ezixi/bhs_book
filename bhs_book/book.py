from ebooklib import epub
import psycopg2
import re
from pathlib import Path
import local_settings


class BhsBook(epub.EpubBook):
    def __init__(self, identifier, title, author, language="en"):
        epub.EpubBook.__init__(self)
        self.set_identifier(identifier)
        self.set_title(title)
        self.set_language(language)
        self.add_author(author)

        self.title = title
        self.author = author
        self.identifier = identifier
        self.language = language
        self.path = self.create_folder()
        self.connection = self.connect_to_db()

    def create_folder(self):
        folder_name = self.title.replace(" ", "-")
        path = f"/Users/martinbell/Desktop/{folder_name}"
        try:
            Path(path).mkdir()
        except FileExistsError:
            pass
        return path

    def connect_to_db(self):
        conn = psycopg2.connect(
            f"dbname={local_settings.LOCALDB} user={local_settings.LOCALUSER}"
        )
        return conn

    def write_book(self):
        self.add_item(epub.EpubNcx())
        self.add_item(epub.EpubNav())
        epub.write_epub(self.path, self)
        return
