from django.forms import ModelForm, Textarea, TextInput
from .models import BlogPost, Tag, Comment

class BlogPostForm(ModelForm):
    
    class Meta:
        model = BlogPost
        fields = [
            'title',
            'content',
            'tags',
        ]

        help_texts = {
            "tags": ("Hold down “Ctrl”, or “Command” on a Mac, to select more than one."),
        }
        widgets = {
            "title": TextInput(attrs={'class':'form-control'}),
            "content": Textarea(attrs={'class':'textarea form-control'})

        }




class TagForm(ModelForm):

    class Meta:
        model = Tag
        fields = '__all__'

    

class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['content',]