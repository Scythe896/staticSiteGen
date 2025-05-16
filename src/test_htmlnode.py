import unittest
from htmlnode import HTMLNode, LeafNode

class testHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"key1": "value1", "key2": "value2"})
        node2 = HTMLNode()
        self.assertEqual(node.props_to_html(), ' key1="value1" key2="value2"')
        self.assertEqual(node2.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("tag", "value", "children", {"key1": "value1"})
        self.assertEqual(node.__repr__(), "HTMLNode(tag, value, children, {'key1': 'value1'})")

class testLeafNode(unittest.TestCase):
    def test_to_html(self):
        full_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(full_node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        p_node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(p_node.to_html(), "<p>This is a paragraph of text.</p>")
        no_value_node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            no_value_node.to_html()
        no_tag_node = LeafNode(None, "Five")
        self.assertEqual(no_tag_node.to_html(), "Five")

if __name__ == "__main__":
    unittest.main()