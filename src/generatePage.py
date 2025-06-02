import os
from htmlnode import HTMLNode
from markdown import markdown_to_blocks, markdown_to_html_node

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.strip("# ")
    raise ValueError("No h1 heading")

def generate_page(from_path, template_path, destination_path):
    print(f"Generating page from {from_path} to {destination_path} using {template_path}")
    with open(from_path) as f:
        markdown_contents = f.read()
    with open(template_path) as f:
        template_contents = f.read()
    node = markdown_to_html_node(markdown_contents)
    html = node.to_html()
    title = extract_title(markdown_contents)
    template_contents = template_contents.replace("{{ Title }}", title).replace("{{ Content }}", html)
    if not os.path.exists(destination_path.split("/")[0]):
        os.makedirs(destination_path.split("/")[0])
    with open(destination_path, "w") as f:
        f.write(template_contents)


