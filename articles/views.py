from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64

from articles.tree_element import TreeElement
from .models import Article,Articlecitation,Articlereference
from .queries import Queries
import json

from articles import Database
from articles.Crawler import Crawler
from articles import ResultsExport
from articles.Article import ObjectEncoder

def find_article(request, url_to_find):
    Database.connect_to_database()
    url_to_find_bytes = base64.b64decode(url_to_find)
    url_to_find = url_to_find_bytes.decode('ascii')
    entry = Article.objects.get(url=url_to_find)
    queries = Queries()
    ResultsExport.export_to_javascript(entry)
    f = open('tree.json')
    data = json.load(f)
    return JsonResponse(data)


def crawl_article(request, url_to_crawl):
    Database.connect_to_database()
    url_to_find_bytes = base64.b64decode(url_to_crawl)
    url_to_crawl = url_to_find_bytes.decode('ascii')
    article = Crawler().crawl_url(url=url_to_crawl)

    ResultsExport.export_to_json(article=article)

    Database.insert_article_to_database(title=article.title, url=article.url, date=article.date,
                                        publisher=article.publisher, citation_count=article.citation_count,
                                        reference_count=article.reference_count)

    Database.insert_references_to_database(article=article)
    Database.insert_citations_to_database(article=article)
    return HttpResponse("URL crawled")

def crawl_null_articles(request):
    Database.connect_to_database()
    null_elements = Database.get_elements_from_database_with_null_citations()
    for element in null_elements:
        article = Crawler().crawl_url(element[1])
        Database.update_article_in_database(article)
        Database.insert_references_to_database(article=article)
        Database.insert_citations_to_database(article=article)
def index(request):
    return HttpResponse("hello from index")


