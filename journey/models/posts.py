from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

# Create your models here
class Post(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travelblog_posts')
    image_url = models.URLField(blank=True)
    visited_places = models.CharField(max_length=100)
    visited_date = models.DateField('Date')
    favorite_place = models.CharField(max_length=250, blank=True, help_text='Optional')
    address = models.CharField(max_length=500, blank=True, help_text='Optional')
    favorite_activity = models.CharField(max_length=250, blank=True, help_text='Optional')
    description = RichTextField(blank=True, help_text='Optional')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
