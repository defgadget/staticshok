import unittest

from blocknode import *


class TestBlockNode(unittest.TestCase):
    def test_block_to_paragraph(self):
        text = "this is a paragraph"
        node = block_to_block_type(text)
        expect = BlockNode("this is a paragraph", block_type_paragraph)
        self.assertEqual(node, expect)

    def test_block_to_heading(self):
        text = "# this is a heading"
        node = block_to_block_type(text)
        expect = BlockNode("# this is a heading", block_type_heading)
        self.assertEqual(node, expect)

        text = "#### this is a heading"
        node = block_to_block_type(text)
        expect = BlockNode("#### this is a heading", block_type_heading)
        self.assertEqual(node, expect)

        text = "####### this is not a heading"
        node = block_to_block_type(text)
        expect = BlockNode("####### this is not a heading", block_type_paragraph)
        self.assertEqual(node, expect)

    def test_block_to_unord_list(self):
        text = "* item 1\n* item 2"
        node = block_to_block_type(text)
        expect = BlockNode(text, block_type_unordered_list)
        self.assertEqual(node, expect)

        text = "- item 1\n- item 2"
        node = block_to_block_type(text)
        expect = BlockNode(text, block_type_unordered_list)
        self.assertEqual(node, expect)

        text = "*item 1\n* item 2"
        node = block_to_block_type(text)
        expect = BlockNode(text, block_type_paragraph)
        self.assertEqual(node, expect)

        text = "-item 1\n- item 2"
        node = block_to_block_type(text)
        expect = BlockNode(text, block_type_paragraph)
        self.assertEqual(node, expect)

    def test_block_to_ord_list(self):
        text = "1. item 1\n2. item 2"
        node = block_to_block_type(text)
        expect = BlockNode(text, block_type_ordered_list)
        self.assertEqual(node, expect)

        text = "1. item 1\n3. item 2"
        node = block_to_block_type(text)
        expect = BlockNode(text, block_type_paragraph)
        self.assertEqual(node, expect)

        text = "1.item 1\n3. item 2"
        node = block_to_block_type(text)
        expect = BlockNode(text, block_type_paragraph)
        self.assertEqual(node, expect)

    def test_block_to_code(self):
        text = "```item 1\n2. item 2```\n"
        node = block_to_block_type(text)
        expect = BlockNode(text, block_type_code)
        self.assertEqual(node, expect)

    def test_block_to_quote(self):
        text = ">item 1\n> item 2```\n"
        node = block_to_block_type(text)
        expect = BlockNode(text, block_type_quote)
        self.assertEqual(node, expect)
