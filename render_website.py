import json
from jinja2 import Environment, FileSystemLoader

with open("books/meta_data.json", encoding="utf-8") as file:
    books = json.load(file)

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index.html")

html = template.render(books=books)

with open("index.html", "w", encoding="utf-8") as file:
    file.write(html)

print(f"Сгенерировано {len(books)} карточек")
