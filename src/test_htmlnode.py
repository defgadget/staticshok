import unittest

from htmlnode import *


class TestTextNode(unittest.TestCase):
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

    def test_simple_markdown_to_html(self):
        text = "This is a simple paragraph"
        html = markdown_to_html(text)
        expect = ParentNode("div", [LeafNode("p", "This is a simple paragraph")])
        self.assertEqual(html, expect)

    def test_compliex_markdown_to_html(self):
        text = """
# This is a heading

```
This is code
```

* Item 1
* Item 2

1. Item 1
2. Item 2

>This is quoted
>text.

This is a paragraph
"""
        html = markdown_to_html(text)
        expect = ParentNode(
            "div",
            [
                LeafNode("h1", "# This is a heading\n"),
                ParentNode("pre", [LeafNode("code", "```\nThis is code\n```\n")]),
                ParentNode(
                    "ul", [LeafNode("li", "* Item 1"), LeafNode("li", "* Item 2")]
                ),
                ParentNode(
                    "ol", [LeafNode("li", "1. Item 1"), LeafNode("li", "2. Item 2")]
                ),
                LeafNode("blockquote", ">This is quoted\n>text.\n"),
                LeafNode("p", "This is a paragraph\n"),
            ],
        )
        self.assertEqual(html, expect)

    def test_extract_title(self):
        text = "# This is my title"
        title = extract_title(text)
        self.assertEqual(title, text)

        self.assertRaises(Exception, msg="no header in this file")


if __name__ == "__main__":
    unittest.main()
