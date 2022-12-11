from django import forms
from .models import Comment, Cocomment

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content' : forms.Textarea(attrs={'maxlength' : 500,})
        }
    def clean_content(self):
        content=self.cleaned_data.get('content','')
        bad_words = [
            '씨발', '좆', '씹', '자지', '보지', '개새',
            '씨부랄', '부랄', '씨팔', '니미', '니애미',
            '느금', '니애비', 'ㅈ같', '샹년', '시발', '시바', '씨바',
            '씨8', '시8', '십8',
            ]
        for w in bad_words:
            if w in content:
                content = content.replace(w, '*'*len(w))
        return content


class CocommentModelForm(CommentModelForm):
    pass

