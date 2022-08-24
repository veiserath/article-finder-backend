import json
from collections import deque
from articles import Database
from articles.tree_element import TreeElement


def construct_tree(entry):
    unique_article_titles = set()
    queue = deque()
    root = TreeElement(name=entry.title, url=entry.url, date=entry.date, publisher=entry.publisher, citation_count=entry.citation_count, references_count=entry.reference_count, children=[])
    queue.append(root)
    while queue:
        current = queue.popleft()
        if current.name not in unique_article_titles:
            add_children(current)
            unique_article_titles.add(current.name)
        for child in current.children:
            queue.append(child)
    return root


def add_children(node):
    unique_children = []
    for child in Database.get_children_one_level(node):
        unique_children.append(child)
    node.children = unique_children


def export_to_javascript(entry):
    root = construct_tree(entry)
    result_json = '{"root": '
    result_json += root.toJSON()
    result_json += "}"
    with open("tree.json", "w") as outfile:
        outfile.write(result_json)


def export_to_json(article):
    paper_info = {
        'title': article.title,
        'url': article.url,
        'date': article.date,
        'publisher': article.publisher,
        'citation count': article.citation_count,
        'reference count': article.reference_count,
        'references': article.references,
        'citations': article.citations
    }
    result_json = json.dumps(paper_info)
    with open("result.json", "w") as outfile:
        outfile.write(result_json)
