from django import forms
from .models import Comment, Post, Category


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


'''choices = Category.objects.all().values_list('name', 'name')
choice_list = []
for item in choices:
    choice_list.append(item)
'''

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('categories', 'title', 'body', 'post_image', 'tags')
        #widgets = {'categories': forms.Select(choices=choice_list)}


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('categories', 'title', 'body', 'post_image')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')


class SearchForm(forms.Form):
    query = forms.CharField()