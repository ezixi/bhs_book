from bhs_book.book import BhsBook
from bhs_book.story import BhsStory


def main():
    book = BhsBook(
        identifier="backhandstories.com-one",
        title="Backhand Stories: Anthology One",
        author="Martin Bell",
    )

    replacement_rules = {
        r"<\!\-*\w*\-*\>": "",
        r"--": " — ",
        r"(?:\\+\w)+": "</p><p>",
        r"\\": "",
    }
    story_ids = [27, 45]
    connection = book.connect_to_db()
    book_folder = book.create_folder()
    for story_id in story_ids:
        story = BhsStory(story_id, replacement_rules)
        content = story.get_story(story_id, connection)
        story_title = content[0]
        story_body = story.clean_story(content[1])
        story.write_html(
            book_folder, story_title, story_body, story_ids.index(story_id)
        )

    connection.close()
    # book.collate_chapters(paths)
    return


if __name__ == "__main__":
    main()
