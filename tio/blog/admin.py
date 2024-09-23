# blog/admin.py

from django.contrib import admin
from .models import Post, Category, Comment
# from .forms import CustomUserChangeForm, CustomUserCreationForm
# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin

# CustomUser = get_user_model()


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    fields = ('title', 'scripture', 'exegesis', 'application', 'category', 'image', 'author')


# class CustomAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = [
#         'email',
#         'username',
#         'is_superuser',
#     ]


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
# admin.site.register(CustomUser, CustomAdmin)
