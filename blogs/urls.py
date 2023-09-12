from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [

    path('tags/', views.TagList.as_view(), name='tag_list'),
    path('tags/create/', views.TagCreate.as_view(), name='tag_create'),

    path('', views.BlogPostList.as_view(), name='blogpost_list'),
    path('tags/<slug:slug>/', views.TagBlogPostList.as_view(), name='tag_blogpost_list'),
    path('user/<slug:slug>', views.AuthorBlogPostList.as_view(), name='author_blogpost_list'),
    path('saved/', views.SavedBlogPostList.as_view(), name='saved_blogpost_list'),

    path('create/', views.BlogPostCreate.as_view(), name='blogpost_create'),
    path('<slug:slug>/', views.BlogPostDetail.as_view(), name='blogpost_detail'),
    path('update/<slug:slug>/', views.BlogPostUpdate.as_view(), name='blogpost_update'),
    path('delete/<slug:slug>/', views.BlogPostDelete.as_view(), name='blogpost_delete'),

    path('create-comment/<slug:slug>/<str:content>/', views.create_comment, name='create_comment'),
    path('delete-comment/<int:commentId>/', views.delete_comment, name='delete_comment'),

    path('save-blogpost/<slug:slug>/', views.save_blogpost, name='save_blogpost'),
]
