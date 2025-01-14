from extractmarkdownimages import extract_markdown_images
from extractmarkdownlinks import extract_markdown_links
from textnode import TextNode, TextType
from splitnodesdelimiter import split_nodes_delimiter
from parentnode import ParentNode
import re

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        image_pairs = extract_markdown_images(node.text)
        remainder = node.text

        for pair in image_pairs:
            match_string = f"![{pair[0]}]({pair[1]})"
            [left, right] = remainder.split(match_string)
            remainder = right
            if len(left) > 0:
                new_nodes.append(TextNode(left, TextType.TEXT))
            new_nodes.append(TextNode(pair[0], TextType.IMAGE, pair[1]))

        if len(remainder) > 0:
            new_nodes.append(TextNode(remainder, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        image_pairs = extract_markdown_links(node.text)
        remainder = node.text

        for pair in image_pairs:
            match_string = f"[{pair[0]}]({pair[1]})"
            [left, right] = remainder.split(match_string)
            remainder = right
            if len(left) > 0:
                new_nodes.append(TextNode(left, TextType.TEXT))
            new_nodes.append(TextNode(pair[0], TextType.LINK, pair[1]))

        if len(remainder) > 0:
            new_nodes.append(TextNode(remainder, TextType.TEXT))

    return new_nodes

def tap(func):
    def inner(value):
        func(value)
        return value
    return inner

def pipe(*args):
    def inner(value):
        holder = value
        for fn in args:
            holder = fn(holder)

        return holder
    
    return inner


def text_to_textnodes(text):
    return pipe(
        lambda n: split_nodes_delimiter(n, "**", TextType.BOLD),
        lambda n: split_nodes_delimiter(n, "*", TextType.ITALIC),
        lambda n: split_nodes_delimiter(n, "`", TextType.CODE),
        split_nodes_image,
        split_nodes_link
    )([TextNode(text, TextType.TEXT)])

def markdown_to_blocks(markdown):
    return list(filter(
        lambda s: len(s) > 0, 
        list(map(
            lambda b: b.strip(),
            markdown.split("\n\n")
        ))
    ))

def block_to_block_type(block):
    matches = re.findall(r"^(#{1,6})", block)
    if len(matches) > 0:
        return "heading"
    
    lines = block.split("\n")

    if block.startswith("```") and block.endswith("```"):
        return "code"
    
    if all(map(lambda s: s.startswith(">"), lines)):
        return "quote"
    
    if all(map(lambda s: s.startswith("* ") or s.startswith("- "), lines)):
        return "unordered_list"
    
    if all(map(lambda s: re.search("^\d+\.", s) != None, lines)):
        return "ordered_list"
    
    return "paragraph"

def parent_block_factory(block_text, block_type):
    if block_type == "heading":
        hash_counts = block_text.count("#", 0, 7)
        return ParentNode(
            f"h{hash_counts}",
            text_to_textnodes(block_text.lstrip("# "))
        )
    
    if block_type == "code":
        modified_text = re.sub(r"^`{3}|`{3}$", "", block_text)
        return ParentNode(
            "code",
            text_to_textnodes(modified_text)
        )
    
    if block_type == "quote":
        modified_text = re.sub(r"\n> ", "\n", block_text)
        return ParentNode(
            "blockquote",
            text_to_textnodes(modified_text)
        )
    
    if block_type == "unordered_list":
        list_items = pipe(
            lambda full_text: re.sub(r"\n[-*] ", "\n", full_text).split("\n"),
            lambda lines: list(map(
                pipe(
                    lambda text: text_to_textnodes(text),
                    lambda child_nodes: ParentNode('li', child_nodes)
                ),
                lines
            ))
        )(block_text)
        return ParentNode('ul', list_items)
    
    if block_type == "ordered_list":
        list_items = pipe(
            lambda full_text: re.sub(r"\n\d+\. ", "\n", full_text).split("\n"),
            lambda lines: list(map(
                pipe(
                    lambda text: text_to_textnodes(text),
                    lambda child_nodes: ParentNode('li', child_nodes)
                ),
                lines
            ))
        )(block_text)
        return ParentNode('ol', list_items)

    if block_type == "paragraph":
        return ParentNode('p', text_to_textnodes(block_text))

    raise Exception("unsupported block type")


def blocks_to_document(block_and_parent_types):
    return ParentNode(
        'div',
        list(map(lambda pair: parent_block_factory(*pair), block_and_parent_types))
    )

def markdown_to_html(markdown):
    return pipe(
        lambda md: markdown_to_blocks(md),
        lambda md_blocks: list(map(lambda bl: [bl, block_to_block_type(bl)], md_blocks)),
        blocks_to_document
    )(markdown)
