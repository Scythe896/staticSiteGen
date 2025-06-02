import os
import shutil
from textnode import TextNode
from generatePage import generate_page

def static_to_public(src, destination):
    print(f"Looking for {destination}")
    if not os.path.exists(destination):
        print("Not Found making directory")
        os.mkdir(destination)
    else:
        print("Found removing files")
        shutil.rmtree(destination)
        os.mkdir(destination)
    src_list = os.listdir(src)
    for item in src_list:
        item_path = f"{src}/{item}"
        destination_path = f"{destination}/{item}"
        print(f"Examining: {item_path}")
        if os.path.isfile(item_path):
            print(f"Copying file: {item_path} to {destination_path}")
            shutil.copy(item_path, destination_path)
        else:
            print(f"Calling function on {item_path} and {destination_path}")
            static_to_public(item_path, destination_path)
    


def main():
    static_to_public("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

main()

