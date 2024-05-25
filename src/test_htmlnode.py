import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {"href": "http://boot.dev", "some": "other"}
        node = HTMLNode(tag="a", props=props)
        props_string = node.props_to_html()

        expected = ' href: "http://boot.dev" some: "other"'
        self.assertEqual(props_string, expected)

    def test_create_node(self):
        node = HTMLNode("a", "b", None, None)
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "b")
        self.assertIsNone(node.props)
        self.assertIsNone(node.children)

    def test_leaf_node_render_html(self):
        props = {"href": "http://boot.dev", "some": "other"}
        node = LeafNode(tag="p", value="some text", props=props)
        html = node.to_html()
        expected = f'<p href: "http://boot.dev" some: "other">some text</p>'
        self.assertEqual(html, expected)

    def test_parent_node_render_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        html = node.to_html()
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(html, expected)

    def test_nested_parent_nodes(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node2 = ParentNode(
            "div",
            [node],
        )
        expected = (
            "<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>"
        )
        html = node2.to_html()
        self.assertEqual(html, expected)


if __name__ == "__main__":
    unittest.main()
