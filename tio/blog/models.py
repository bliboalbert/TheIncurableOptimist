# blog/models.py
import uuid
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# class CustomUser(AbstractUser):
#     pass


class Post(models.Model):
    # uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    # slug = models.SlugField(max_length=200, unique=True, editable=False)
    title = models.CharField(max_length=200)
    scripture = RichTextField()  # Daily scripture
    exegesis = RichTextField() # Metaphysical exegesis
    application = RichTextField()  # Daily application of the scripture
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    tags = TaggableManager()
    is_featured = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.uuid})

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         if self.title:
    #             self.slug = slugify(self.title)
    #         else:
    #             self.slug = slugify(str(self.uuid))
    #     super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class PostView(models.Model):
    post = models.ForeignKey(Post, related_name='post_views', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ip_address} viewed {self.post.title}'


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.author}'

