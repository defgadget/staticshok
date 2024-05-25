import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_links,
    text_to_textnodes,
)
from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_split_on_delim(self):
        node = TextNode("Some *text* here", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(len(new_nodes), 3)

        expected_nodes = [
            TextNode("Some ", text_type_text),
            TextNode("text", text_type_italic),
            TextNode(" here", text_type_text),
        ]

        self.assertListEqual(new_nodes, expected_nodes)

        node = TextNode("Some *text*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(len(new_nodes), 2)

        expected_nodes = [
            TextNode("Some ", text_type_text),
            TextNode("text", text_type_italic),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

        node = TextNode("*Some* text", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(len(new_nodes), 2)

        expected_nodes = [
            TextNode("Some", text_type_italic),
            TextNode(" text", text_type_text),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_no_closing_delim(self):
        node = TextNode("*Some text", text_type_text)
        new_node = split_nodes_delimiter([node], "*", text_type_italic)
        expected = TextNode("*Some text", text_type_text)
        self.assertListEqual(new_node, [expected])
        self.assertEqual(len(new_node), 1)

    def test_extract_image(self):
        text = "![image](https://image.com)"
        images = extract_markdown_images(text)
        expect = [("image", "https://image.com")]
        self.assertListEqual(images, expect)

    def test_extract_multi_image(self):
        text = "![image](https://image.com) ![another](https://another.com)"
        images = extract_markdown_images(text)
        expect = [("image", "https://image.com"), ("another", "https://another.com")]
        self.assertListEqual(images, expect)

    def test_extract_links(self):
        text = "[link](https://image.com)"
        links = extract_markdown_links(text)
        expect = [("link", "https://image.com")]
        self.assertListEqual(links, expect)

    def test_extract_multi_links(self):
        text = "[image](https://image.com) [another](https://another.com)"
        links = extract_markdown_links(text)
        expect = [("image", "https://image.com"), ("another", "https://another.com")]
        self.assertListEqual(links, expect)

    def test_split_image(self):
        node = TextNode(
            "This is an image ![link](https://image.com) more text", text_type_text
        )
        new_nodes = split_nodes_image([node])
        expect = [
            TextNode("This is an image ", text_type_text),
            TextNode("link", text_type_image, "https://image.com"),
            TextNode(" more text", text_type_text),
        ]
        self.assertListEqual(new_nodes, expect)

        node = TextNode("![link](https://image.com) more text", text_type_text)
        new_nodes = split_nodes_image([node])
        expect = [
            TextNode("link", text_type_image, "https://image.com"),
            TextNode(" more text", text_type_text),
        ]
        self.assertListEqual(new_nodes, expect)

        node = TextNode("This is an image ![link](https://image.com)", text_type_text)
        new_nodes = split_nodes_image([node])
        expect = [
            TextNode("This is an image ", text_type_text),
            TextNode("link", text_type_image, "https://image.com"),
        ]
        self.assertListEqual(new_nodes, expect)

    def test_split_multi_image(self):
        node = TextNode(
            "This is an image ![link](https://image.com) more text ![another](https://another.com) the end",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        expect = [
            TextNode("This is an image ", text_type_text),
            TextNode("link", text_type_image, "https://image.com"),
            TextNode(" more text ", text_type_text),
            TextNode("another", text_type_image, "https://another.com"),
            TextNode(" the end", text_type_text),
        ]
        self.assertListEqual(new_nodes, expect)

        node = TextNode(
            "![link](https://image.com) more text ![another](https://another.com) the end",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        expect = [
            TextNode("link", text_type_image, "https://image.com"),
            TextNode(" more text ", text_type_text),
            TextNode("another", text_type_image, "https://another.com"),
            TextNode(" the end", text_type_text),
        ]
        self.assertListEqual(new_nodes, expect)

        node = TextNode(
            "This is an image ![link](https://image.com) more text ![another](https://another.com)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        expect = [
            TextNode("This is an image ", text_type_text),
            TextNode("link", text_type_image, "https://image.com"),
            TextNode(" more text ", text_type_text),
            TextNode("another", text_type_image, "https://another.com"),
        ]
        self.assertListEqual(new_nodes, expect)

        node = TextNode(
            "![link](https://image.com) more text ![another](https://another.com)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        expect = [
            TextNode("link", text_type_image, "https://image.com"),
            TextNode(" more text ", text_type_text),
            TextNode("another", text_type_image, "https://another.com"),
        ]
        self.assertListEqual(new_nodes, expect)

    def test_split_link(self):
        node = TextNode(
            "This is an image [link](https://image.com) more text", text_type_text
        )
        new_nodes = split_nodes_links([node])
        expect = [
            TextNode("This is an image ", text_type_text),
            TextNode("link", text_type_link, "https://image.com"),
            TextNode(" more text", text_type_text),
        ]
        self.assertListEqual(new_nodes, expect)

        node = TextNode("[link](https://image.com) more text", text_type_text)
        new_nodes = split_nodes_links([node])
        expect = [
            TextNode("link", text_type_link, "https://image.com"),
            TextNode(" more text", text_type_text),
        ]
        self.assertListEqual(new_nodes, expect)

        node = TextNode("This is an image [link](https://image.com)", text_type_text)
        new_nodes = split_nodes_links([node])
        expect = [
            TextNode("This is an image ", text_type_text),
            TextNode("link", text_type_link, "https://image.com"),
        ]
        self.assertListEqual(new_nodes, expect)

    def test_split_multi_link(self):
        node = TextNode(
            "This is an image [link](https://image.com) more text [another](https://another.com) the end",
            text_type_text,
        )
        new_nodes = split_nodes_links([node])
        expect = [
            TextNode("This is an image ", text_type_text),
            TextNode("link", text_type_link, "https://image.com"),
            TextNode(" more text ", text_type_text),
            TextNode("another", text_type_link, "https://another.com"),
            TextNode(" the end", text_type_text),
        ]
        self.assertListEqual(new_nodes, expect)

        node = TextNode(
            "[link](https://image.com) more text [another](https://another.com) the end",
            text_type_text,
        )
        new_nodes = split_nodes_links([node])
        expect = [
            TextNode("link", text_type_link, "https://image.com"),
            TextNode(" more text ", text_type_text),
            TextNode("another", text_type_link, "https://another.com"),
            TextNode(" the end", text_type_text),
        ]
        self.assertListEqual(new_nodes, expect)

        node = TextNode(
            "This is an image [link](https://image.com) more text [another](https://another.com)",
            text_type_text,
        )
        new_nodes = split_nodes_links([node])
        expect = [
            TextNode("This is an image ", text_type_text),
            TextNode("link", text_type_link, "https://image.com"),
            TextNode(" more text ", text_type_text),
            TextNode("another", text_type_link, "https://another.com"),
        ]
        self.assertListEqual(new_nodes, expect)

        node = TextNode(
            "[link](https://image.com) more text [another](https://another.com)",
            text_type_text,
        )
        new_nodes = split_nodes_links([node])
        expect = [
            TextNode("link", text_type_link, "https://image.com"),
            TextNode(" more text ", text_type_text),
            TextNode("another", text_type_link, "https://another.com"),
        ]
        self.assertListEqual(new_nodes, expect)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"

        nodes = text_to_textnodes(text)
        expect = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertListEqual(nodes, expect)
