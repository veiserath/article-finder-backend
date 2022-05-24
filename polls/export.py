from collections import deque
from polls.queries import Queries
from .queries import Queries

class Export:

    def __init__(self) -> None:
        pass


    def add_children(self, node, unique_articles):
        unique_children = []
        for child in Queries().get_children_one_level(node):
            if child.name not in unique_articles:
                unique_children.append(child)
                unique_articles.add(child.name)

        node.children = unique_children

    def construct_tree(self, root):
        unique_article_titles = set()
        queue = deque()
        queue.append(root)
        while queue:
            current = queue.popleft()
            if current.name not in unique_article_titles:
                unique_article_titles.add(current.name)
                self.add_children(current, unique_article_titles)
                for child in current.children:
                    queue.append(child)
        print(unique_article_titles)
        return root

    def export_to_json(self, root=Queries().get_root_object()):
        root = self.construct_tree(root)
        result_json = root.toJSON()
        with open("tree.json", "w") as outfile:
            outfile.write(result_json)