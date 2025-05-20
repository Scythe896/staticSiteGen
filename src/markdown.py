import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # old_nodes is a list of TextNodes
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception("Missing Closing Delimiter")
        for i in range (0, len(split_text)):
            if i % 2 == 0:
                new_nodes.append(TextNode(split_text[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    # returns tuple of anchor and image in format ![anchor](image)
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    # returns tuple of anchor and url in format [anchor](url)
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        links = extract_markdown_links(text)
        for anchor, url in links:
            text = text.replace(f"[{anchor}]({url})", "toSplit")
        split = re.split("(toSplit)", text)
        count = 0
        for section in split:
            if section == "":
                continue
            if section == "toSplit":
                new_nodes.append(TextNode(links[count][0], TextType.LINK, links[count][1]))
                count += 1
            else:
                new_nodes.append(TextNode(section, TextType.TEXT))
    return new_nodes

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        images = extract_markdown_images(text)
        for anchor, img in images:
            text = text.replace(f"![{anchor}]({img})", "toSplit")
        split = re.split("(toSplit)", text)
        count = 0
        for section in split:
            if section == "":
                continue
            if section == "toSplit":
                new_nodes.append(TextNode(images[count][0], TextType.IMAGE, images[count][1]))
                count += 1
            else:
                new_nodes.append(TextNode(section, TextType.TEXT))
    return new_nodes