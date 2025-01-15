from extractmarkdownimages import extract_markdown_images
from extractmarkdownlinks import extract_markdown_links
from textnode import TextNode, TextType
from splitnodesdelimiter import split_nodes_delimiter
from parentnode import ParentNode
from leafnode import LeafNode
import re
import os

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

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    
    if text_node.text_type == TextType.NORMAL:
        return LeafNode(None, text_node.text)
    
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})

    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", text_node.text, {"src": text_node.url})
    
    raise Exception("unknown text_node type")

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
            list(map(text_node_to_html_node, text_to_textnodes(block_text.lstrip("# "))))
        )
    
    if block_type == "code":
        modified_text = re.sub(r"^`{3}|`{3}$", "", block_text)
        return ParentNode(
            "code",
            list(map(text_node_to_html_node, text_to_textnodes(modified_text)))
        )
    
    if block_type == "quote":
        modified_text = re.sub(r"^> ", "", block_text, 0, re.M)
        return ParentNode(
            "blockquote",
            list(map(text_node_to_html_node, text_to_textnodes(modified_text)))
        )
    
    if block_type == "unordered_list":
        list_items = pipe(
            lambda full_text: re.sub(r"^[-*] ", "", full_text, 0, re.M).split("\n"),
            lambda lines: list(map(
                pipe(
                    lambda text: text_to_textnodes(text),
                    lambda child_nodes: ParentNode('li', list(map(text_node_to_html_node, child_nodes)))
                ),
                lines
            ))
        )(block_text)
        return ParentNode('ul', list_items)
    
    if block_type == "ordered_list":
        list_items = pipe(
            lambda full_text: re.sub(r"^\d+\. ", "", full_text, 0, re.M).split("\n"),
            lambda lines: list(map(
                pipe(
                    lambda text: text_to_textnodes(text),
                    lambda child_nodes: ParentNode('li', list(map(text_node_to_html_node, child_nodes)))
                ),
                lines
            ))
        )(block_text)
        return ParentNode('ol', list_items)

    if block_type == "paragraph":
        return ParentNode('p', list(map(text_node_to_html_node, text_to_textnodes(block_text))))

    raise Exception("unsupported block type")


def blocks_to_document(block_and_parent_types):
    return ParentNode(
        'div',
        list(map(lambda pair: parent_block_factory(*pair), block_and_parent_types))
    )

def markdown_to_html(markdown):
    return pipe(
        lambda md: markdown_to_blocks(md),
        lambda md_blocks: list(map(
            lambda bl: [bl, block_to_block_type(bl)],
            md_blocks
        )),
        blocks_to_document
    )(markdown)

def extract_title(markdown):
    match = re.search(r"(?:^#|\n#) ([^\n]+)", markdown)
    if match == None:
        raise Exception("no h1 header found in markdown")
    
    return match[1].strip(" ")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if os.path.isfile(from_path) != True:
        raise Exception(f"{from_path} is not a file")
    
    file_obj = open(from_path)
    markdown = file_obj.read()
    file_obj.close()

    if os.path.isfile(template_path) != True:
        raise Exception(f"{template_path} is not a file")
    
    file_obj = open(template_path)
    template = file_obj.read()
    file_obj.close()

    title = extract_title(markdown)
    block = markdown_to_html(markdown)

    content = block.to_html()
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    file_obj = open(dest_path, mode='w')
    file_obj.write(template)
    file_obj.close()
