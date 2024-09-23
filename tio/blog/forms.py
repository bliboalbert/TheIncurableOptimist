# blog/forms.py

from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'body']


class NewsletterForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email', 'class': 'form-control'
    }))
