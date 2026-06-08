import json
from jinja2 import Environment, FileSystemLoader
from livereload import Server


def on_reload():
    with open("books/meta_data.json", encoding="utf-8") as file:
        books = json.load(file)

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index.html")

    html = template.render(books=books)

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(html)

    print(f"Сгенерерировано {len(books)} карточек")


server = Server()
server.watch("templates/index.html", on_reload)
server.serve(root=".", host="127.0.0.1", port=5500)
