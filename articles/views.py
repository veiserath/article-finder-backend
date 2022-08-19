from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64

from articles.tree_element import TreeElement
from .models import Article,Articlecitation,Articlereference
from .queries import Queries
from .export import Export
import json

from articles import Database
from articles.Crawler import Crawler
from articles import ResultsExport

def find_article(request, url_to_find):
    Database.connect_to_database()
    url_to_find_bytes = base64.b64decode(url_to_find)
    url_to_find = url_to_find_bytes.decode('ascii')
    entry = Article.objects.get(url=url_to_find)
    queries = Queries()
    # articles = queries.get_elements_from_database_with_citations()
    main_article_url = entry.url

    children_of_main_article = []
    for citation in Articlecitation.objects.filter(main_article_url=entry.url):
        try:
            article = Article.objects.get(url=citation.citation_article_url)
            children_of_main_article.append(article)
        except Article.DoesNotExist:
            continue
    Export().export_to_json(root=TreeElement(name=entry.title,url=entry.url, citation_count=entry.citation_count, children=children_of_main_article))
    f = open('tree.json')
    data = json.load(f)
    Database.close_connection()
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
    Database.close_connection()
    return HttpResponse("URL crawled")

def crawl_null_articles(request):
    Database.connect_to_database()
    null_elements = Database.get_elements_from_database_with_null_citations()
    for element in null_elements:
        article = Crawler().crawl_url(element[1])
        Database.update_article_in_database(article)
        Database.insert_references_to_database(article=article)
        Database.insert_citations_to_database(article=article)
    Database.close_connection()
def index(request):
    return HttpResponse("hello from index")


