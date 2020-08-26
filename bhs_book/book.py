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

    def create_folder(self):
        folder_name = self.title.replace(" ", "-")
        path = distutils.dir_util.mkpath(f"/tmp/{folder_name}")
        return path

    def connect_to_db(self):
        conn = psycopg2.connect(
            f"dbname={local_settings.LOCALDB} user={local_settings.LOCALUSER}"
        )
        return conn
