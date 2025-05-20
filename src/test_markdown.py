import unittest
from textnode import TextNode, TextType
from markdown import (split_nodes_delimiter, extract_markdown_images,
                      extract_markdown_links, split_nodes_link,
                      split_nodes_images)

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