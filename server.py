import argparse
import json
from pathlib import Path
from urllib.parse import quote
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader
from livereload import Server


BOOKS_PER_PAGE = 20
BOOKS_PER_ROW = 2
REDIRECT_HTML = """\
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=pages/index1.html">
  <title>Онлайн библиотека</title>
</head>
<body>
  <p><a href="pages/index1.html">Онлайн библиотека</a></p>
</body>
</html>"""


def parse_args():
    parser = argparse.ArgumentParser(description="Онлайн библиотека")
    parser.add_argument(
        "--data",
        default="media/meta_data.json",
        help="Путь к метаданным книг (по умолчанию: media/meta_data.json)",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Адрес сервера (по умолчанию: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5500,
        help="Порт сервера (по умолчанию: 5500)",
    )
    return parser.parse_args()


def on_reload(data_path):
    media_root = str(Path(data_path).parent)
    with open(data_path, encoding="utf-8") as file:
        books = json.load(file)

    for book in books:
        book["book_url"] = quote(media_root + "/" + book["book_path"])
        book["img_url"] = quote(book["img_src"])
        book["genres"] = [
            g.strip().rstrip(".")
            for g in book.get("genres", "").split(",")
            if g.strip()
        ]

    pages = list(chunked(books, BOOKS_PER_PAGE))

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index.html")

    Path("pages").mkdir(exist_ok=True)

    total_pages = len(pages)
    for page_num, page_books in enumerate(pages, 1):
        book_pairs = list(chunked(page_books, BOOKS_PER_ROW))
        html = template.render(
            books=book_pairs,
            current_page=page_num,
            total_pages=total_pages,
            prev_page=page_num - 1 if page_num > 1 else None,
            next_page=page_num + 1 if page_num < total_pages else None,
        )
        with open(
            f"pages/index{page_num}.html", "w", encoding="utf-8"
        ) as file:
            file.write(html)

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(REDIRECT_HTML)


def main():
    args = parse_args()
    server = Server()
    server.watch("templates/index.html", lambda: on_reload(args.data))
    server.serve(root=".", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
