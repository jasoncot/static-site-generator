import re

def extract_markdown_links(text):
    pairs = []
    matches = re.findall(r"\[(.*?)\]\(([^ )]+?)(?: (.*?))?\)", text)

    for i in range(0, len(matches)):
        pairs.append(matches[i])

    return pairs