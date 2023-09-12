from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Count
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse

from django.utils.text import slugify

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages

from .models import BlogPost, Tag, Comment
from .forms import BlogPostForm, TagForm, CommentForm




###############   LISTING     #################

class BlogPostList(generic.ListView):

    model = BlogPost
    template_name = 'blogs/blogpost_list.html'


class TagBlogPostList(generic.ListView):

    template_name = 'blogs/blogpost_list_tag.html'
    def get_queryset(self):
        tag = Tag.objects.get(slug = self.kwargs.get('slug'))
        return tag.posts.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug = self.kwargs.get('slug')).name
        return context

    
    

class AuthorBlogPostList(generic.ListView):

    def get_template_names(self):
        if self.request.user == User.objects.get(username = self.kwargs.get('slug')):
            template_name =  'blogs/blogpost_list_user.html'
        else:
            template_name =  'blogs/blogpost_list_author.html'
        
        return template_name
    

    def get_queryset(self):
        return BlogPost.objects.filter(author__username = self.kwargs.get('slug'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.kwargs.get('slug')
        return context





class SavedBlogPostList(LoginRequiredMixin, generic.ListView):

    login_url = "users:login"

    template_name = 'blogs/blogpost_list_saved.html'
    def get_queryset(self):
        user = self.request.user
        return user.favorites.all()
    


#################    BLOGPOST OPERATIONS    #################


class BlogPostDetail(generic.DetailView):


    template_name = 'blogs/blogpost_detail.html'
    model = BlogPost
    


class BlogPostCreate(LoginRequiredMixin, generic.CreateView):

    login_url = "users:login"

    template_name = 'blogs/blogpost_create.html'
    model = BlogPost
    form_class = BlogPostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

        


class BlogPostUpdate(LoginRequiredMixin, generic.UpdateView):

    login_url = "users:login"

    template_name = 'blogs/blogpost_update.html'
    model = BlogPost
    form_class = BlogPostForm


class BlogPostDelete(LoginRequiredMixin, generic.DeleteView):

    login_url = "users:login"

    model = BlogPost
    success_url = 'blogs:blogpost_list'

    def get_success_url(self):
        return reverse_lazy('blogs:blogpost_list')
    
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    


def save_blogpost(request, slug):
    if request.user.is_authenticated:
        blogpost = BlogPost.objects.get(slug=slug)

        if request.user in blogpost.saved_by.all():
            blogpost.saved_by.remove(request.user)
            response_message = "Removed from saved posts."

        else:
            blogpost.saved_by.add(request.user)
            response_message = "Added to saved posts."

        return JsonResponse(response_message, safe=False)
    
    else:
        messages.error(request, "You have to login to save Posts.")

        return JsonResponse("Loginsene pic", safe=False)


###################     TAG OPERATIONS     ####################


class TagCreate(LoginRequiredMixin, generic.CreateView):

    template_name = 'blogs/tag_create.html'
    model = Tag
    form_class = TagForm

    login_url = "users:login"

    def form_valid(self, form):

        stop_limit = 3
        tags_created_by_user = self.request.session.get('tags_created_by_user', 0)

        if tags_created_by_user >= stop_limit:
            messages.warning(self.request, 'Yavaş la kaç tane açiyon.')
            return redirect('blogs:tag_list')
        
        self.request.session['tags_created_by_user'] = tags_created_by_user + 1
        return super().form_valid(form)


class TagList(generic.ListView):

    template_name = 'blogs/tag_list.html'

    def get_queryset(self):
        return Tag.objects.all().annotate(count = Count('posts')).order_by('-count')



class TagDelete(generic.DeleteView):

    model = Tag
    success_url = reverse_lazy('blogs:tag_list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    



################    COMMENT OPERATIONS    ################



def create_comment(request, slug, content):

    if request.user.is_authenticated:
    
        blogpost = BlogPost.objects.get(slug = slug)
        user = request.user
        blogpost.comment_set.create(user = user, content = content)
        return JsonResponse('helal sana goca gıral', safe=False)

    else:
        messages.error(request, "You have to login to comment.")
        return JsonResponse("Loginsene pic", safe=False)
    


def delete_comment(request, commentId):


    comment = Comment.objects.get(id = commentId)

    if request.user == comment.user:

        comment.delete()
        return JsonResponse('aferim', safe=False)
    
    else:
        messages.error(request, "You have to login to delete your comment.")
        return JsonResponse("Loginsene pic", safe=False)
    