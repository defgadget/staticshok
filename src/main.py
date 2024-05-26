import os
import pathlib
import shutil

from markdown_blocks import markdown_to_html_node


def main():
    # generate_page("./content/index.md", "./template.html", "./public/index.html")
    generate_pages_recursive("./content/", "./template.html", "./public/")
    # move_files("./static", "./public")


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
        if os.path.isfile(item_from_path) and os.path.splitroot:
            print(f"copying {item_from_path} to {item_to_path}")
            shutil.copy(item_from_path, item_to_path)
        elif os.path.isdir(item_from_path):
            move_files(item_from_path, item_to_path)
        else:
            raise Exception(f"don't recognize {item} as file or dir")


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("no header in this file")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_contents = ""
    with open(from_path, "r") as from_file:
        from_contents = from_file.read()

    template_contents = ""
    with open(template_path, "r") as template_file:
        template_contents = template_file.read()

    title = extract_title(from_contents)
    contents = markdown_to_html_node(from_contents).to_html()

    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", contents)

    # dirs = os.path.dirname(dest_path)
    # os.makedirs(dirs, exist_ok=True)

    with open(dest_path, "w") as dest_file:
        dest_file.write(template_contents)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    to_path = pathlib.Path(dest_dir_path)
    from_path = pathlib.Path(dir_path_content)

    if not from_path.exists():
        raise Exception(f"the path {dir_path_content} does not exist")

    if not to_path.exists():
        # print(f"creating {dest_dir_path}")
        to_path.mkdir()

    dir_items = os.listdir(dir_path_content)
    for item in dir_items:
        origin = from_path.joinpath(item)
        dest = to_path.joinpath(item)
        # print(f"org: {origin} dest: {dest}")

        if origin.is_dir():
            # print(f"origin is {origin} making directory {dest}")
            if not origin.exists():
                dest.mkdir()
            generate_pages_recursive(f"{origin}", template_path, f"{dest}")
        elif origin.is_file() and origin.suffix == ".md":
            to_file = to_path.joinpath(f"{dest.stem}.html")
            # print(
            #     f"found md file {origin} copying to {to_file} using templat {template_path}"
            # )
            generate_page(f"{origin}", template_path, f"{to_file}")


main()
