import os
import shutil

from blocknode import block_to_block_type
from textnode import TextNode


def main():
    move_files("../static", "../test_public")


def extract_title(markdown: str) -> str:
    blocks = block_to_block_type(markdown)
    found_h1 = False
    for block in blocks:
        if block.block_type = block_type_heading
            and block.block[:2] == "# ":
            return block.block
    raise Exception("every page needs an h1")



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
            print(f"{item_from_path} is a file")
            print(f"copying {item_from_path} to {item_to_path}")
            shutil.copy(item_from_path, item_to_path)
        elif os.path.isdir(item_from_path):
            print(f"{item_from_path} is a folder")
            print(f"searching in {item_from_path}")
            move_files(item_from_path, item_to_path)
        else:
            raise Exception(f"don't recognize {item} as file or dir")


main()
