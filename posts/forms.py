from django import forms
from posts.models import Post, Comment
from mptt.forms import TreeNodeChoiceField

class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'message',)


class CreateCommentForm(forms.ModelForm):

    parent = TreeNodeChoiceField(queryset = Comment.objects.all())

    class Meta:
        model = Comment
        fields = ('text','parent',)
    
    def __init__(self, *args, **kwargs):
        super(CreateCommentForm, self).__init__(*args, **kwargs)
        self.fields['parent'].required = False
