import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()