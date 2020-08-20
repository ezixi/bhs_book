from ebooklib import epub
import psycopg2
import local_settings

book = epub.EpubBook()
book.set_identifier("backhandstories.com-one")
book.set_title("Backhand Stories: Anthology One")
book.set_language("en")
book.add_author("Martin Bell")


def get_story_ids():
    story_ids = [27]
    return story_ids


def connect_to_db():
    conn = psycopg2.connect(
        f"dbname={local_settings.LOCALDB} user={local_settings.LOCALUSER}"
    )
    return conn


def get_story(story_id, connection):
    cur = connection.cursor()
    cur.execute(
        f"""
        SELECT post_title, post_content from wp_posts where "ID" = {story_id};
        """
    )
    return cur.fetchall()


def main():
    connection = connect_to_db()
    for story_id in get_story_ids():
        story = get_story(story_id, connection)
        print(story)
    return


if __name__ == "__main__":
    main()
