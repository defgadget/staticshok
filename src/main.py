import os
import shutil

from htmlnode import markdown_to_html


def main():
    generate_page("./content/index.md", "./template.html", "./public/index.html")


def move_files(from_path: str, to_path) -> None:
    if not os.path.exists(from_path):
        raise Exception(f"the path {from_path} does not exist")

    if not os.path.exists(to_path):
        print(f"creating {to_path}")
        os.mkdir(to_path)

    dir_items = os.listdir(from_path)
    print(f"Files and folders to be copied -- {dir_items}")
    for item in dir_items:
        item_from_path = os.path.join(from_path, item)
        item_to_path = os.path.join(to_path, item)
        if os.path.isfile(item_from_path):
            print(f"copying {item_from_path} to {item_to_path}")
            shutil.copy(item_from_path, item_to_path)
        elif os.path.isdir(item_from_path):
            move_files(item_from_path, item_to_path)
        else:
            raise Exception(f"don't recognize {item} as file or dir")


def extract_title(markdown: str) -> str:
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line
    raise Exception("no header in this file")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as from_file:
        from_contents = from_file.read()

    with open(template_path) as template_file:
        template_contents = template_file.read()

    title = extract_title(from_contents)
    contents = markdown_to_html(from_contents).to_html()

    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", contents)

    dirs = os.path.dirname(dest_path)
    os.makedirs(dirs, exist_ok=True)

    with open(dest_path, "w") as dest_file:
        dest_file.write(template_contents)


main()
