# blog/forms.py

from django import forms
from .models import Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'body']


class NewsletterForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email', 'class': 'form-control'
    }))


# class CustomUserCreationForm(UserCreationForm):
#     model = get_user_model()
#     fields = {
#         'email',
#         'username',
#     }
#
#
# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = get_user_model()
#         fields = {
#             'email',
#             'username',
#         }