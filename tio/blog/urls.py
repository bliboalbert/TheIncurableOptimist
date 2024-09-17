# blog/urls.py

from django.urls import path
from .views import PostListView, PostDetailView, CategoryPostListView, AboutView, ContactView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<int:category_id>/', CategoryPostListView.as_view(), name='category_posts'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
]
