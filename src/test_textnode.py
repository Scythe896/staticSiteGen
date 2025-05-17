import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.LINK)
        node4 = TextNode("This is a text nod", TextType.LINK)
        node5 = TextNode("This is a text node", TextType.BOLD, None)
        node6 = TextNode("This is a text node", TextType.BOLD, "test")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node3, node4)
        self.assertEqual(node, node5)
        self.assertNotEqual(node, node6)

class test_text_node_to_html_node(unittest.TestCase):
    def test_text_node_to_html_node(self):
        node = TextNode("Text Node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.__repr__(), "LeafNode(b, Text Node, None, None)")

if __name__ == "__main__":
    unittest.main()