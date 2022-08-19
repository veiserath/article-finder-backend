import json

from bs4 import BeautifulSoup
from lxml import etree
from articles import paths
from articles.Article import Article
from webdriver_manager.chrome import ChromeDriverManager
import json
from mimetypes import init
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Crawler:

    def __init__(self) -> None:
        self.SOUP = None
        options = Options()
        options.headless = True
        options.add_argument('--disable-gpu')
        options.add_argument("user-agent=Chrome/80.0.3987.132")
        options.add_argument("--window-size=1920,1080")
        self.dr = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    

    def crawl_url(self, url):
        self.dr.get(url)
        self.SOUP = BeautifulSoup(self.dr.page_source,"lxml")
        self.DOM = etree.HTML(str(self.SOUP))
        result = self.get_ld_json()
        article = self.construct_article_object(result)
        return article


    def get_ld_json(self) -> dict:
        return json.loads("".join(self.SOUP.find("script", {"type": "application/ld+json"}).contents))

    def get_references(self, result, citations_range):
        references = []
        for i, item in enumerate(result["citation"]):
            if i >= citations_range:
                break
            paper_info = {
                'title': item["headline"],
                'url': item["mainEntityOfPage"],
                'date': item["datePublished"],
                'publisher': item["publisher"]["name"],
            }
            references.append(paper_info)
        return references


    def get_citations(self, result, citations_range):
        citations = []
        for i in range(citations_range, len(result["citation"])):
            paper_info = {
                'title': result["citation"][i]["headline"],
                'url': result["citation"][i]["mainEntityOfPage"],
                'date': result["citation"][i]["datePublished"],
                'publisher': result["citation"][i]["publisher"]["name"],
            }
            citations.append(paper_info)
        return citations


    def get_count(self, string):
        count = ""
        for item in string:
            if item.isdigit():
                count += item
        return count


    def get_citation_count(self):
        try:
            citation = str(self.DOM.xpath("//div[contains(text(),'Citations')]/text()")[0])
        except IndexError:
            return 0
        return int(self.get_count(citation))


    def get_references_count(self):
        try:
            references = str(self.DOM.xpath("//div[contains(text(),'References')]/text()")[0])
        except IndexError:
            return 0
        return int(self.get_count(references))


    def print_main_article_metadata(self, result):
        print(result["headline"])
        print(result["datePublished"])
        print(result["mainEntityOfPage"])
        # make it a one-liner
        for item in result["author"]:
            print(item["name"])
        print(result["publisher"]["name"])
        print("====")
        print("citation " + str(self.get_citation_count()))
        print("references " + str(self.get_references_count()))


    def print_references(result):
        i = 0
        for item in result["citation"]:
            print(i)
            print(item["headline"])
            print(item["datePublished"])
            print(item["mainEntityOfPage"])
            # make it a one-liner
            for subitem in item["author"]:
                print(subitem["name"])
            print(item["publisher"]["name"])
            i += 1
            print("===")


    def construct_article_object(self, result):
        citations_range = abs(len(result["citation"]) - 1 - self.get_citation_count())
        title = result["headline"]
        url = result["mainEntityOfPage"]
        date = result["datePublished"]
        publisher = result["publisher"]["name"]

        citation_count = int(self.get_citation_count())
        reference_count = int(self.get_references_count())
        references = self.get_references(result, citations_range)
        citations = self.get_citations(result, citations_range)
        article = Article(title=title, url=url, date=date, publisher=publisher, citation_count=citation_count,
                        reference_count=reference_count, references=references, citations=citations)
        print(article.title)
        return article

