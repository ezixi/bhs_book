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
                    <p>Yasunari Kawabata collected some of his writing in a book called ‘Palm-of-the-Hand \
                    Stories.’It was an apt choice; most of the pieces were no more than a hundred words or \
                    so, beautiful, fragile little scenes that took a few seconds to read but stayed with you \
                    far, far longer. The idea was that the stories could fit, literally, in your palm. \
                    Typically Japanese.</p>
                    <p>I, on the other hand, am not Japanese. And I’m far from fragile (but my mum thinks I’m\
                     beautiful. I hope.) When I first created this site, I was writing scenes and short \
                    stories filled with characters I remember from growing up in the suburbs of Manchester, \
                    in the north-west of England. Manchester is generally an industrial city (although I \
                    think it has changed some now) and my family were working people. The people I met in the\
                     street, in the pubs, in the markets and especially those I came across as I followed my \
                    Dad around on his deliveries were more likely to show you the back of their hand (as in, \
                    “Any more lip from you son, an' you’ll see the back o' me hand...!) than consider the \
                    merits of flash fiction crafted by a Japanese Nobel-prize-winning author.</p>
                    <p>Most of the scenes I wrote never materialized into anything more substantial – in \
                    fact, most of them never materialized into anything at all, as they’re all still floating\
                     in the limbo of a corrupted hard drive at the bottom of a cardboard box on my garage \
                    floor. However, I did want to create a place for new writers where short fiction was the \
                    norm, where writers could grow and learn and where you could read work in a couple of \
                    minutes that would stay with you the rest of the day.</p>
                    <p>So there you are. Backhand Stories. I hope you enjoy them.</p>
                    <p>Martin Bell</p>
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
        chapter.content += create_pagebreak("blah")
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
