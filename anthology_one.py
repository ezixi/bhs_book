from ebooklib import epub
from bhs_book.book import BhsBook
from bhs_book.story import BhsStory

book = BhsBook(
    identifier="backhandstories.com-one",
    title="Anthology One",
    author="Martin Bell",
    style_sheet="""
            @namespace epub "http://www.idpf.org/2007/ops";
            body {
                font-family: "Adobe Caslon", Georgia, "Times New Roman", Times, serif;
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

story_ids = [214, 734, 24, 508, 559, 484, 535, 275, 23, 491, 9]

frontmatter = {
    "i": {
        "page": "Title",
        "content": """
            <!doctype html>
                    <html lang="en">
                    <head></head>
                    <body id="title">
                        <h1>Anthology</h1>
                        <h2>Backhand Stories</p>
                    </body>
                </html>
                """,
    },
    "ii": {
        "page": "Introduction",
        "content": """
        <!doctype html>
                <html lang="en">
                <head></head>
                <body>
                    <h1>Introduction</h1>
                    <p>Some Text</p>
                </body>
            </html>
        """,
    },
}

replacement_rules = {
    r"<\!\-*\w*\-*\>": "",
    r"--": " — ",
    r"(?:\\+\w)+": "</p><p>",
    r"\\": "",
    r"###": "</br>",
}


def add_frontmatter(fm):
    for order, text in fm.items():
        title = text["page"]
        filepath = f"{title}-{order}.xhtml"
        chapter = epub.EpubHtml(title=title, file_name=filepath, lang="en")
        chapter.content = text["content"]
        book.add_chapter(chapter)
    return


def add_stories(story_ids):
    for story_id in story_ids:
        story = BhsStory(story_id, replacement_rules, book.connection)
        chapter = story.create_chapter(story_ids.index(story_id) + len(frontmatter))
        book.add_chapter(chapter)
    book.connection.close()
    return


def main():
    add_frontmatter(frontmatter)
    add_stories(story_ids)
    book.write_book()
    return


if __name__ == "__main__":
    main()
