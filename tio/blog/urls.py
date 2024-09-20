# blog/urls.py

from django.urls import path
from .views import (PostListView, PostDetailView, CategoryPostListView, AboutView, ContactView, PostSearchView, TaggedPostListView)
from django.contrib.sitemaps.views import sitemap
from .sitemap import PostSitemap

sitemaps = {'posts': PostSitemap}


urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<int:category_id>/', CategoryPostListView.as_view(), name='category_posts'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('tag/<slug:slug>', TaggedPostListView.as_view(), name='tagged_posts'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
