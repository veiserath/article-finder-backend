from django.contrib import admin

from .models import Article, Articlecitation, Articlereference

admin.site.register(Article)
admin.site.register(Articlecitation)
admin.site.register(Articlereference)