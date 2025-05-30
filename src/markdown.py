import re
from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # old_nodes is a list of TextNodes
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError("Missing Closing Delimiter")
        for i in range (0, len(split_text)):
            if split_text[i] == "":
                continue
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
        if len(links) == 0:
            new_nodes.append(node)
            continue
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
        if len(images) == 0:
            new_nodes.append(node)
            continue
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

def text_to_textnodes(text):
    start_node = [TextNode(text, TextType.TEXT)]
    bold = split_nodes_delimiter(start_node, "**", TextType.BOLD)
    italic = split_nodes_delimiter(bold, "_", TextType.ITALIC)
    code = split_nodes_delimiter(italic, "`", TextType.CODE)
    image = split_nodes_images(code)
    return split_nodes_link(image)

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        new_blocks.append(block)
    return new_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    
    # Check for Heading
    # Boots helped quite a bit here
    if block.startswith("#"):
        header = block.split(" ")[0]
        length = len(header)
        if length <= 6 and len(block) != length:
            if block[length] == " ":
                header = header.replace("#", "")
                if header == "":
                    return BlockType.HEADING

    # Check for Code Block
    if block.startswith("```") and block.endswith("```"):
        sliced = block[3:(len(block)-3)]
        if not sliced.startswith("`") and not sliced.endswith("`"):
            return BlockType.CODE
    
    # Checking for Quote Block
    if block.startswith(">"):
        for i in range(0, len(lines)):
            if not lines[i].startswith(">"):
                break
            if i == len(lines)- 1:
                return BlockType.QUOTE
    
    # Checking for Unordered List
    if block.startswith("- "):
        for i in range(0, len(lines)):
            if not lines[i].startswith("- "):
                break
            if i == len(lines) - 1:
                return BlockType.UNORDERED_LIST
    
    # Checking Ordered List
    if block.startswith("1. "):
        for i in range(0, len(lines)):
            if not lines[i].startswith(f"{i+1}. "):
                break
            if i == len(lines) - 1:
                return BlockType.ORDERED_LIST
    
    # All checks failed returns Paragraph
    return BlockType.PARAGRAPH

def text_to_children(text, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            text = text.replace("\n", " ")
        case BlockType.HEADING | BlockType.QUOTE:
            text = text.split(" ", 1)[1]
        case BlockType.ORDERED_LIST | BlockType.UNORDERED_LIST:
            lines = text.split("\n")
            new_lines = []
            for line in lines:
                line = line.split(" ", 1)[1]
                new_lines.append(f"<li>{line}</li>")
            text = "".join(new_lines)
        case _:
            raise ValueError("Invalid block type")
    text_nodes = text_to_textnodes(text)
    child_nodes = []
    for node in text_nodes:
        child_nodes.append(text_node_to_html_node(node))
    return child_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                block_node = ParentNode("p", None)
            case BlockType.HEADING:
                header = block.split(" ")[0]
                block_node = ParentNode(f"h{header.count("#")}", None)
            case BlockType.QUOTE:
                block_node = ParentNode("blockquote", None)
            case BlockType.CODE:
                child_nodes.append(ParentNode("pre", [LeafNode("code", block.lstrip("```\n").rstrip("```"))]))
                continue
            case BlockType.ORDERED_LIST:
                block_node = ParentNode("ol", None)
            case BlockType.UNORDERED_LIST:
                block_node = ParentNode("ul", None)
            case _:
                raise ValueError("No block type")
        block_node.children = text_to_children(block, block_type)
        child_nodes.append(block_node)
    return ParentNode("div", child_nodes)