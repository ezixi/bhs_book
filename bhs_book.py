from ebooklib import epub
import psycopg2
import local_settings


class BhsBook(epub.EpubBook):
    def __init__(self, identifier, title, author, language="en"):
        book = epub.EpubBook()
        book.set_identifier(identifier)
        book.set_title(title)
        book.set_language(language)
        book.add_author(author)

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

    def write_html(self, title, story):
        path = f"/tmp/{title}.html"
        with open(path, "w") as f:
            body = f"""
                <!DOCTYPE html>
                        <html lang="en">
                        <head></head>
                        <body>
                            <h1>{title}</h1>
                            {story}
                        </body>
                    </html>
            """
            f.write(body)
        return path


def main():
    new_book = BhsBook(
        identifier="backhandstories.com-one",
        title="Backhand Stories: Anthology One",
        author="Martin Bell",
    )
    story_ids = [27]
    connection = new_book.connect_to_db()
    for story_id in story_ids:
        data = new_book.get_story(story_id, connection)
        new_book.write_html(data[0], data[1])
    connection.close()
    return


if __name__ == "__main__":
    main()
