import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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
        p_node = LeafNode("p", "This is a paragraph of text.")
        no_value_node = LeafNode("p", None)
        no_tag_node = LeafNode(None, "Five")
        self.assertEqual(full_node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        self.assertEqual(p_node.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(no_tag_node.to_html(), "Five")
        with self.assertRaises(ValueError):
            no_value_node.to_html()
        
class testParentNode(unittest.TestCase):
    def test_to_html(self):
        child1 = LeafNode("b", "LeafChild1")
        child2 = LeafNode("i", "LeafChild2")
        child3 = LeafNode("b", "LeafChild3")
        one_child = ParentNode("p", [child1])
        three_child = ParentNode("p", [child1, child2, child3])
        grand_child = ParentNode("p", [one_child])
        grand_children = ParentNode("p", [one_child, three_child, child2])
        self.assertEqual(one_child.to_html(), "<p><b>LeafChild1</b></p>")
        self.assertEqual(three_child.to_html(), "<p><b>LeafChild1</b><i>LeafChild2</i><b>LeafChild3</b></p>")
        self.assertEqual(grand_child.to_html(), "<p><p><b>LeafChild1</b></p></p>")
        self.assertEqual(grand_children.to_html(), "<p><p><b>LeafChild1</b></p><p><b>LeafChild1</b><i>LeafChild2</i><b>LeafChild3</b></p><i>LeafChild2</i></p>")

if __name__ == "__main__":
    unittest.main()