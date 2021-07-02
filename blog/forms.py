from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=30, help_text='Input name')
    to = forms.EmailField(help_text='Input receiver email')
    comment = forms.CharField(required=False, widget=forms.Textarea,
                              help_text='Also you may send some comment')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')
