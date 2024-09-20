# blog/views.py

from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q

from .models import Post, Category, Comment
from .forms import CommentForm


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
        context['related_posts'] = Post.objects.filter(category=self.object.category).exclude(id=self.object.id)[:3]
        return context

    def get(self, request, *args, **kwargs):

        post = self.get_object()
        post.views += 1
        post.save(update_fields=['views'])
        return super().get(request, *args, **kwargs)

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


class TaggedPostListView(ListView):
    model = Post
    template_name = 'blog/tagged_post.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('slug')
        return context


# 4. TemplateView for the About page
class AboutView(TemplateView):
    template_name = 'blog/about.html'


# 5. TemplateView for the Contact page
class ContactView(TemplateView):
    template_name = 'blog/contact.html'


class PostSearchView(ListView):
    model = Post
    template_name = 'blog/post_search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(Q(title__icontains=query) | Q(exegesis__icontains=query))
        return Post.objects.none()
