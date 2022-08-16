from django import forms
from .models import Comment, Cocomment

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class CocommentModelForm(forms.ModelForm):
    class Meta:
        model = Cocomment
        fields = ['content']

