# blog/views.py

from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from .models import Post, Category, PostView
from .forms import CommentForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import NewsletterForm
from .newsletter_util import subscribe_email_to_mailchimp


# from ratelimit.decorators import ratelimit


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        # Add categories to the context for filtering
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        """Override this method to customize the query."""
        return Post.objects.all().order_by('-created_at')  # Show most recent posts first

    def get(self, request, *args, **kwargs):
        # If this is an AJAX request, handle pagination dynamically
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            page = request.GET.get('page')
            posts = self.get_queryset()
            paginator = Paginator(posts, self.paginate_by)
            try:
                posts = paginator.page(page)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

            # Return only the rendered posts HTML
            posts_html = self.render_to_string('blog/post_partial_list.html', {'posts': posts})
            return JsonResponse({'posts_html': posts_html})

        return super().get(request, *args, **kwargs)

    def render_to_string(self, template_name, context):
        """Helper function to render template as a string for AJAX requests."""
        from django.template.loader import render_to_string
        return render_to_string(template_name, context)


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

    def get_client_ip(self, request):
        # Helper method to get the client's IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get(self, request, *args, **kwargs):
        post = self.get_object()

        # Get the user's IP address
        ip_address = self.get_client_ip(request)

        # Check if this IP has viewed the post before
        if not PostView.objects.filter(post=post, ip_address=ip_address).exists():
            # If not, increment the view count and log the IP
            post.views += 1
            post.save(update_fields=['views'])
            # Save the view record
            PostView.objects.create(post=post, ip_address=ip_address)

        # Proceed with the usual `get` behavior
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


# @ratelimit(key='ip', rate='5/m', method='GET', block=True)
# def my_view(request):
#     return HttpResponse("This view is rate limited to 5 requests per minute.")


class NewsletterSubscribeView(FormView):
    template_name = 'newsletter_subscribe.html'
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter_subscribe')

    def form_valid(self, form):
        email = form.cleaned_data['email']

        # Subscribe email to Mailchimp
        status_code, response_json = subscribe_email_to_mailchimp(email)

        if status_code == 200:
            # Send confirmation email
            send_mail(
                'Thank you for subscribing!',
                'You have successfully subscribed to our newsletter.',
                'your_email@example.com',
                [email],
                fail_silently=False,
            )

            # Show success message on the website
            messages.success(self.request, 'You have successfully subscribed to our newsletter!')
        else:
            # If Mailchimp subscription fails
            messages.error(self.request, 'There was an issue subscribing. Please try again.')

        # Redirect to success URL
        return super().form_valid(form)

    def form_invalid(self, form):
        # Show error message if the form is invalid
        messages.error(self.request, 'Invalid email. Please try again.')
        return super().form_invalid(form)
