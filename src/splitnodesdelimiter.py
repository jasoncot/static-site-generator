from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) == 1:
            new_nodes.append(node)
            continue

        for i in range(0, len(parts)):
            if i % 2 == 0:
                # these are text nodes
                if len(parts[i]) > 0:
                    new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i], text_type))
                
    return new_nodes