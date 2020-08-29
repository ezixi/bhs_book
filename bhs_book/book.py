from ebooklib import epub
import psycopg2
import re
from pathlib import Path
import local_settings


class BhsBook(epub.EpubBook):
    def __init__(self, identifier, title, author, style_sheet, language="en"):
        super().__init__()
        self.set_identifier(identifier)
        self.set_title(title)
        self.set_language(language)
        self.add_author(author)

        self.title = title
        self.author = author
        self.identifier = identifier
        self.style_sheet = style_sheet
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
        conn = psycopg2.connect(f"dbname={local_settings.LOCALDB} user={local_settings.LOCALUSER}")
        return conn

    def add_chapter(self, chapter):
        self.add_item(chapter)
        self.toc.append(chapter)
        self.spine.append(chapter)
        return

    def write_styles(self):
        css = epub.EpubItem(
            uid="style_nav", file_name="style/nav.css", media_type="text/css", content=self.style_sheet
        )
        return css

    def write_book(self):
        self.add_item(self.write_styles())
        self.add_item(epub.EpubNcx())
        self.add_item(epub.EpubNav())
        epub.write_epub(f"{self.path}/{self.title}.epub", self)
        return
