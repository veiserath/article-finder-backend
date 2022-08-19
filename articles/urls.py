from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('crawl_article/<str:url_to_crawl>/', views.crawl_article, name='crawl_article'),
    path('find_article/<str:url_to_find>/', views.find_article, name='find_article'),
    path('crawl_null_articles/', views.crawl_null_articles, name='crawl_null_articles'),
]