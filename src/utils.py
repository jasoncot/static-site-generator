from extractmarkdownimages import extract_markdown_images
from extractmarkdownlinks import extract_markdown_links
from textnode import TextNode, TextType

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
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

