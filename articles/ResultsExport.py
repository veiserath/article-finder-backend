import json
from collections import deque
from articles import Database


def construct_tree():
    unique_article_titles = set()
    queue = deque()

    root = Database.get_root_object()
    queue.append(root)

    while queue:
        current = queue.popleft()
        if current.name not in unique_article_titles:
            unique_article_titles.add(current.name)
            add_children(current, unique_article_titles)
            for child in current.children:
                queue.append(child)
    print(unique_article_titles)
    return root

# dac mu dzialac przez 5 sekund i znalezc petle
def add_children(node, unique_articles):
    unique_children = []
    for child in Database.get_children_one_level(node):
        if child.name not in unique_articles:
            unique_children.append(child)
            unique_articles.add(child.name)

    node.children = unique_children
    # node.children = Database.get_children_one_level(node)


def export_to_javascript():
    root = construct_tree()
    result_json = "root = "
    result_json += root.toJSON()
    with open("tree.js", "w") as outfile:
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
