# Generated by Django 4.0.1 on 2022-02-11 14:18

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('journey', '0003_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, help_text='Optional'),
        ),
        migrations.AlterField(
            model_name='post',
            name='favorite_place',
            field=models.CharField(blank=True, help_text='Optional', max_length=250),
        ),
    ]
