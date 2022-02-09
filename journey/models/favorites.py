from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models

from journey.models.posts import Post


class Favorites(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Favorted by {self.user.first_name} on {self.created}'
