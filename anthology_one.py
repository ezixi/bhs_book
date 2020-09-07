from ebooklib import epub
from ebooklib.utils import create_pagebreak
from bhs_book.book import BhsBook
from bhs_book.story import BhsStory

book = BhsBook(
    identifier="backhandstories.com-one",
    title="Anthology",
    author="Martin Bell",
    style_sheet="""
            @namespace epub "http://www.idpf.org/2007/ops";
            body {
                font-family: "Adobe Caslon", Georgia, "Times New Roman", Times, serif;
                text-align: justify;
            }
            h1 {
                 text-align: left;
                 text-transform: uppercase;
                 font-weight: 200;
            }

            p {
                padding-bottom: 1em;
            }
            ol {
                list-style-type: none;
            }
            ol > li:first-child {
                    margin-top: 0.3em;
            }
            nav[epub|type~='toc'] > ol > li > ol  {
                list-style-type:square;
            }
            nav[epub|type~='toc'] > ol > li > ol > li {
                    margin-top: 0.3em;
            }
        """,
)

story_ids = [793, 794, 214, 734, 24, 508, 559, 484, 535, 275, 23, 491, 9]


replacement_rules = {
    r"<\!\-*\w*\-*\>": "",
    r"--": " — ",
    r"(?:\\+\w)+": "</p>\n<p>",
    r"\\": "",
    r"#+": "</br>",
}


def add_stories(story_ids):
    for story_id in story_ids:
        story = BhsStory(story_id, replacement_rules, book.connection)
        chapter = story.create_chapter(story_ids.index(story_id))
        book.add_chapter(chapter)
    book.connection.close()
    return


def main():
    add_stories(story_ids)
    book.write_book()
    return


if __name__ == "__main__":
    main()
