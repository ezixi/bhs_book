from ebooklib import epub
import psycopg2
import local_settings


class BhsBook(epub.EpubBook):
    def __init__(self):
        book = epub.EpubBook()
        book.set_identifier("backhandstories.com-one")
        book.set_title("Backhand Stories: Anthology One")
        book.set_language("en")
        book.add_author("Martin Bell")

    def get_story_ids(self):
        story_ids = [27]
        return story_ids

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
        return cur.fetchall()


def main():
    book = BhsBook()
    connection = book.connect_to_db()
    for story_id in book.get_story_ids():
        story = book.get_story(story_id, connection)
        print(story)
    return


if __name__ == "__main__":
    main()
