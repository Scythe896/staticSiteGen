import os
import shutil
from markdown import markdown_to_blocks, markdown_to_html_node

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

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.strip("# ")
    raise ValueError("No h1 heading")

def generate_page(from_path, template_path, destination_path, base_path):
    print(f"Generating page from {from_path} to {destination_path} using {template_path}")
    with open(from_path) as f:
        markdown_contents = f.read()
    with open(template_path) as f:
        template_contents = f.read()
    node = markdown_to_html_node(markdown_contents)
    html = node.to_html()
    title = extract_title(markdown_contents)
    template_contents = template_contents.replace("{{ Title }}", title).replace("{{ Content }}", html)
    template_contents = template_contents.replace('href="/', f'href="{base_path}').replace('src="/', f'src="{base_path}')
    if not os.path.exists(destination_path.split("/")[0]):
        os.makedirs(destination_path.split("/")[0])
    with open(destination_path, "w") as f:
        f.write(template_contents)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    content_list = os.listdir(dir_path_content)
    for item in content_list:
        item_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_path) and item.split(".")[1] == "md":
            generate_page(item_path, template_path, os.path.join(dest_dir_path, "index.html"), base_path)
        else:
            os.mkdir(dest_path)
            generate_pages_recursive(item_path, template_path, dest_path, base_path)
