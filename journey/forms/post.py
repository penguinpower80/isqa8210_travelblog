import logging

import django.db.models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div, HTML
from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput

from journey.models import Post


class PostForm(forms.ModelForm):
    image_upload_field = forms.ImageField(required=False)
    # https://django-crispy-forms.readthedocs.io/en/latest/layouts.html
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'title',
                Div(
                    Fieldset(
                        'Image*',
                        Field('image_url'),
                        Field('image_upload_field'),
                        HTML("""
                        <p><strong>You can either specify an image url or upload your own image. If you supply both, the uploaded image will take precedence.</strong></p>
                    """)
                    ),
                    css_class="p-3 border",
                ),
                'visited_places',
                'visited_date',
                'favorite_place',
                'address',
                'favorite_activity',
                'description'
            ),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn btn-outline-dark text-white')
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        image_url = cleaned_data.get('image_url')
        image_file = cleaned_data.get('image_upload_field')
        if image_url == "" and image_file is None:
            raise ValidationError('You must supply either an image url or upload an image file.')

    class Meta:
        model = Post
        fields = (
            'title',
            'image_url',
            'image_upload_field',
            'visited_places',
            'visited_date',
            'favorite_place',
            'address',
            'favorite_activity',
            'description')
        # Reference - https://stackoverflow.com/questions/41224035/django-form-field-label-how-to-change-its-value-if-it-belongs-to-a-certain-fi
        labels = {'visited_date': "Visited Date"}
        # Reference https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django
        widgets = {'visited_date': DateInput(attrs={'type': 'date', 'placeholder': 'Select a date'})}
