from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import random

# Create your models here.


class PublishedPost(models.Manager):
    def get_queryset(self):
        return super(PublishedPost, self).get_queryset().filter(status=True)


class UnpublishedPost(models.Manager):
    def get_queryset(self):
        return super(UnpublishedPost, self).get_queryset().filter(status=False)


class Post(models.Model):
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    title = models.CharField('title post' ,max_length=150)
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='post author')
    short_description = models.CharField('short description',max_length=255,null=True,blank=True)
    descrption = models.TextField()
    image = models.ImageField(upload_to='image/')
    category = models.ManyToManyField('Category') 
    tag = models.ManyToManyField('Tag',null=True,blank=True)
    like = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField('publish', default=True)
    objects = models.Manager()
    Published = PublishedPost()
    Unpublished = UnpublishedPost()
   
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title
    
    def random_number_generator(self):
        return '-' + str(random.randint(1000, 9999))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            while Post.objects.filter(slug = self.slug):
                self.slug = slugify(self.title)
                self.slug += self.random_number_generator()
        return super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="post_comment")    
    owner = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='comment_owner')
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=400)   
    like = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner} commented on {self.post}"


class Category(models.Model):
    title = models.CharField('title category' ,max_length=255)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField('The_title' ,max_length=255)

    class Meta : 
        verbose_name_plural = "post_tags"
        verbose_name = "tags"
        db_table = 'tag'
        ordering = ['-title',]
        
    def __str__(self):
        return self.title
