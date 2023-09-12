from django.db import models
from django.contrib.auth.models import User

from django.utils.text import slugify
from django.urls import reverse
from django.utils import  timezone

# Create your models here.


class Tag(models.Model):

    name = models.CharField(max_length=31)
    slug = models.SlugField(blank=True, unique=True, db_index=True, editable=False)


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blogs:tag_blogpost_list", kwargs={"slug": self.slug})
    


class BlogPost(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=63)
    content = models.TextField()
    
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(Tag, blank=True,related_name='posts')
    saved_by = models.ManyToManyField(User, blank=True,related_name='favorites')
    
    slug = models.SlugField(blank=True, unique=True, db_index=True, editable=False)


    class Meta:
        ordering = ['-last_updated_time']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blogs:blogpost_detail", kwargs={"slug": self.slug})
    
    @property
    def is_saved(self, username):
        return self.saved_by.filter(username=username).exists()
    


class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    content = models.TextField()

    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.content