from ebooklib import epub

book = epub.EpubBook()
book.set_identifier("backhandstories.com-one")
book.set_title("Backhand Stories: Anthology One")
book.set_language("en")
book.add_author("Martin Bell")


def get_story_ids():
    story_ids = [27]
    return story_ids
