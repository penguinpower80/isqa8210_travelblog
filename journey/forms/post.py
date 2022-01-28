from django import forms
from django.forms import DateInput

from journey.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title', 'image_url', 'visited_places', 'visited_date', 'favorite_place', 'address', 'favorite_activity',
            'description')
        # Reference - https://stackoverflow.com/questions/41224035/django-form-field-label-how-to-change-its-value-if-it-belongs-to-a-certain-fi
        labels = {'visited_date': "Visited Date"}
        # Reference https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django
        widgets = {'visited_date': DateInput(attrs={'type': 'date', 'placeholder': 'Select a date'})}
