# Generated by Django 4.0.1 on 2022-02-11 16:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('journey', '0004_alter_post_description_alter_post_favorite_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]
