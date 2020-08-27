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
    for story_id in story_ids:
        story = BhsStory(story_id, replacement_rules)
        story.get_story(book.connection)
        story.clean_story()
        story.write_html()
        chapter = story.create_chapter(story_ids.index(story_id))
        book.add_item(chapter)
    book.connection.close()
    book.write_book()
    return


if __name__ == "__main__":
    main()
