from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')


# class Category(models.Model):
#     name=models.CharField(max_length=250)
#     slug=models.SlugField(max_length=250)
#     def __str__(self):
#         pass

#     class Meta:
#         db_table = ''
#         managed = True
#         verbose_name = 'Category'
#         verbose_name_plural = 'Categories'

class Post(models.Model):
    STATUS_CHOICES=(
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=250,unique_for_date='publish')
    author=models.ForeignKey(User,related_name='blog_posts',on_delete=models.CASCADE)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    tag=TaggableManager()
    published=PublishedManager()
    category=models.CharField(max_length=250,default='')

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,self.publish.month,self.publish.day,self.slug])
    

    def __str__(self):
        return self.title

    class Meta:
        ordering=['-publish']
        db_table = ''
        managed = True
        verbose_name = 'post'
        verbose_name_plural = 'posts'

class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

    class Meta:
        ordering=['-created']
        db_table = ''
        managed = True
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
