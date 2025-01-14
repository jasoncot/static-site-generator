from extractmarkdownimages import extract_markdown_images
from extractmarkdownlinks import extract_markdown_links
from textnode import TextNode, TextType
from splitnodesdelimiter import split_nodes_delimiter

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