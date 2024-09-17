# blog/admin.py

from django.contrib import admin
from .models import Post, Category, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    fields = ('title', 'scripture', 'exegesis', 'application', 'category', 'image', 'author')


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
