import unittest
from textnode import TextNode, TextType
from markdown import (BlockType, split_nodes_delimiter, extract_markdown_images,
                      extract_markdown_links, split_nodes_link,
                      split_nodes_images, text_to_textnodes, markdown_to_blocks,
                      block_to_block_type, markdown_to_html_node)

class test_split_nodes_delimiter(unittest.TestCase):
    def test_single_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),
                                    TextNode("code block", TextType.CODE),
                                    TextNode(" word", TextType.TEXT),])
    
    def test_triple_split(self):
        node = TextNode("one **two** three **four** five **six** seven", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("one ", TextType.TEXT),
                                     TextNode("two", TextType.BOLD),
                                     TextNode(" three ", TextType.TEXT),
                                     TextNode("four", TextType.BOLD),
                                     TextNode(" five ", TextType.TEXT),
                                     TextNode("six", TextType.BOLD),
                                     TextNode(" seven", TextType.TEXT)])

    def test_two_nodes(self):
        node1 = TextNode("one `two` three", TextType.TEXT)
        node2 = TextNode("four `five` six", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("one ", TextType.TEXT),
                                     TextNode("two", TextType.CODE),
                                     TextNode(" three", TextType.TEXT),
                                     TextNode("four ", TextType.TEXT),
                                     TextNode("five", TextType.CODE),
                                     TextNode(" six", TextType.TEXT)])
        
    def test_non_text_type(self):
        node = TextNode("hello **there**", TextType.BOLD)
        node1 = TextNode("one **two** three", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node1], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node, TextNode("one ", TextType.TEXT),
                                     TextNode("two", TextType.BOLD),
                                     TextNode(" three", TextType.TEXT)])
        
    def test_missing_delimiter(self):
        node = TextNode("hello **there world", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter(node, "**", TextType.BOLD)

class test_extract_markdown(unittest.TestCase):
    def test_extract_images(self):
        text = "Hello there ![alt text](image) at ![alt2](img2)"
        self.assertEqual(extract_markdown_images(text),[("alt text", "image"), ("alt2", "img2")])

    def test_extract_links(self):
        text = "Text link [anchor](site) and [anchor2](site2)"
        self.assertEqual(extract_markdown_links(text),[("anchor", "site"), ("anchor2", "site2")])

class test_split_nodes_link(unittest.TestCase):
    def test_split_links(self):
        node = TextNode("hello [anchor](url) at [anchor2](url2)", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [TextNode("hello ", TextType.TEXT),
                                                    TextNode("anchor", TextType.LINK, "url"),
                                                    TextNode(" at ", TextType.TEXT),
                                                    TextNode("anchor2", TextType.LINK, "url2")])
    
    def test_split_images(self):
        node = TextNode("hello ![anchor](img) at ![anchor2](img2)", TextType.TEXT)
        self.assertEqual(split_nodes_images([node]), [TextNode("hello ", TextType.TEXT),
                                                    TextNode("anchor", TextType.IMAGE, "img"),
                                                    TextNode(" at ", TextType.TEXT),
                                                    TextNode("anchor2", TextType.IMAGE, "img2")])
        
class test_text_to_textnodes(unittest.TestCase):
    def test(self):
        text = "Text **bold** _italic_ `code` ![anchor](img) [anchor](url)"
        self.assertEqual(text_to_textnodes(text), [TextNode("Text ", TextType.TEXT),
                                                   TextNode("bold", TextType.BOLD),
                                                   TextNode(" ", TextType.TEXT),
                                                   TextNode("italic", TextType.ITALIC),
                                                   TextNode(" ", TextType.TEXT),
                                                   TextNode("code", TextType.CODE),
                                                   TextNode(" ", TextType.TEXT),
                                                   TextNode("anchor", TextType.IMAGE, "img"),
                                                   TextNode(" ", TextType.TEXT),
                                                   TextNode("anchor", TextType.LINK, "url")])
        
class tests(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        def test_block_to_block_type(self):
            heading_block = "###### hello"
            false_heading = "####### too many #"
            code_block = "```testing\ntesting\ntesting\n```"
            false_code = "```testing\ntesting\ntesting\n``"
            quote_block = "> hello\n> there new\n> padawan"
            false_quote = "> hello\n> there new\n- padawan"
            unordered_block = "- hello\n- there new\n- padawan"
            false_unordered = "- hello\n> there new\n- padawan"
            ordered_block = "1. one\n2. two\n3. three"
            false_ordered = "1. one\n2. two\n4. three"
            self.assertEqual(block_to_block_type(heading_block), BlockType.HEADING)
            self.assertEqual(block_to_block_type(false_heading), BlockType.PARAGRAPH)
            self.assertEqual(block_to_block_type(code_block), BlockType.CODE)
            self.assertEqual(block_to_block_type(false_code), BlockType.PARAGRAPH)
            self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)
            self.assertEqual(block_to_block_type(false_quote), BlockType.PARAGRAPH)
            self.assertEqual(block_to_block_type(unordered_block), BlockType.UNORDERED_LIST)
            self.assertEqual(block_to_block_type(false_unordered), BlockType.PARAGRAPH)
            self.assertEqual(block_to_block_type(ordered_block), BlockType.ORDERED_LIST)
            self.assertEqual(block_to_block_type(false_ordered), BlockType.PARAGRAPH)

        def test_paragraphs(self):
            md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )

        def test_codeblock(self):
            md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )

        def test_header(self):
            md = "### Header _italic_"
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(html, "<div><h3>Header <i>italic</i></h3></div>")

        def test_unordered_list(self):
            md = """
- One
- Two
- Three
"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(html, "<div><ul><li>One</li><li>Two</li><li>Three</li></ul></div>")
        
        def test_link(self):
            md = "This is a paragraph with [a link](https://www.example.com)"
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(html, '<div><p>This is a paragraph with <a href="https://www.example.com">a link</a></p></div>')