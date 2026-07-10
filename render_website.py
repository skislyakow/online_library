import json
from pathlib import Path
from urllib.parse import quote

from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader


BOOKS_PER_PAGE = 20

with open("media/meta_data.json", encoding="utf-8") as file:
    books = json.load(file)

for book in books:
    book["book_url"] = quote("media/" + book["book_path"])
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
    book_pairs = list(chunked(page_books, 2))
    html = template.render(
        books=book_pairs,
        current_page=page_num,
        total_pages=total_pages,
        prev_page=page_num - 1 if page_num > 1 else None,
        next_page=page_num + 1 if page_num < total_pages else None,
    )
    with open(f"pages/index{page_num}.html", "w", encoding="utf-8") as file:
        file.write(html)

redirect = """<!DOCTYPE html>
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
with open("index.html", "w", encoding="utf-8") as file:
    file.write(redirect)

print(f"Сгенерировано {total_pages} страниц, {len(books)} книг")
