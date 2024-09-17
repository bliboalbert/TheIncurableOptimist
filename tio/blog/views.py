# blog/views.py

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.detail import SingleObjectMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Post, Category, Comment
from .forms import CommentForm


# 1. ListView for the Homepage: List all blog posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        # Add categories to the context for filtering
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


# 2. DetailView for viewing individual posts and comments
class PostDetailView(DetailView, FormView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        # Add comments and form to the context
        context = super().get_context_data(**kwargs)
        context['comments'] = self.get_object().comments.all()
        context['comment_form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        # Handle comment form submission
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()
            return redirect(self.object.get_absolute_url())
        else:
            return self.form_invalid(form)


# 3. ListView for listing posts filtered by category
class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        # Get posts only within the selected category
        category = get_object_or_404(Category, pk=self.kwargs['category_id'])
        return Post.objects.filter(category=category).order_by('-created_at')

    def get_context_data(self, **kwargs):
        # Add categories and selected category to the context
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = get_object_or_404(Category, pk=self.kwargs['category_id'])
        return context


# 4. TemplateView for the About page
class AboutView(TemplateView):
    template_name = 'blog/about.html'


# 5. TemplateView for the Contact page
class ContactView(TemplateView):
    template_name = 'blog/contact.html'
