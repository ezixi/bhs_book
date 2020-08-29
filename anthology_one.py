from ebooklib import epub
from bhs_book.book import BhsBook
from bhs_book.story import BhsStory


def main():
    book = BhsBook(
        identifier="backhandstories.com-one",
        title="Anthology One",
        author="Martin Bell",
        style_sheet="""
            @namespace epub "http://www.idpf.org/2007/ops";
            body {
                font-family: Cambria, Liberation Serif, Bitstream Vera Serif,\
                 Georgia, Times, Times New Roman, serif;
            }
            h1 {
                 text-align: left;
                 text-transform: uppercase;
                 font-weight: 200;
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

    replacement_rules = {r"<\!\-*\w*\-*\>": "", r"--": " — ", r"(?:\\+\w)+": "</p><p>", r"\\": ""}

    story_ids = [9, 271]
    for story_id in story_ids:
        story = BhsStory(story_id, replacement_rules, book.connection)
        chapter = story.create_chapter(story_ids.index(story_id))
        book.add_chapter(chapter)
    book.connection.close()
    book.write_book()
    return


if __name__ == "__main__":
    main()
