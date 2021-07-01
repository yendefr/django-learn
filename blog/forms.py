from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=30, help_text='Input name')
    email = forms.EmailField(help_text='Input your email')
    to = forms.EmailField(help_text='Input receiver email')
    comment = forms.CharField(required=False, widget=forms.Textarea,
                              help_text='Also you may send some comment')
