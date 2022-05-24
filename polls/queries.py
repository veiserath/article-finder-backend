from .tree_element import TreeElement

class Queries:

    def __init__(self) -> None:
        pass

    def get_citations_with_main_url(self, url):
        from .models import Article
        students = Article.objects.raw(
                                        "select distinct * from article,articlecitation where article.url = citation_article_url and "
                                        "articlecitation.main_article_url = (%(url)s) and article.citation_count is not null", {'url': url})
        return students


    def get_children_one_level(self, node):
        children_list_of_strings = self.get_citations_with_main_url(node.url)
        list_of_children_as_objects = []
        for element in children_list_of_strings:
            list_of_children_as_objects.append(TreeElement(name=element.title, url=element.url, citation_count=element.citation_count, children=[]))
        return list_of_children_as_objects


    def get_elements_from_database_with_citations(self):
        from .models import Article
        articles = Article.objects.exclude(citation_count__isnull=True)
        return articles

    def get_root_object(self):
        first_element_from_database = self.get_elements_from_database_with_citations()[0]
        root = TreeElement(name=first_element_from_database.title, url=first_element_from_database.url, citation_count=first_element_from_database.citation_count, children=[])
        return root