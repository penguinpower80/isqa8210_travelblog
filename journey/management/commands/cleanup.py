import time

from faker.generator import random

from journey.models import Post, Comment
from django.contrib.auth import get_user_model

from django.core.management import BaseCommand
from django_seed import Seed


class Command(BaseCommand):
    help = "Clear all users(except admin), posts, and comments."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('Deleting Journey data...')

        self.stdout.write('Deleting Posts...')
        Post.objects.all().delete()

        self.stdout.write('Deleting Comments...')
        Comment.objects.all().delete()

        User = get_user_model()
        self.stdout.write('Deleting all regular users...')
        User.objects.filter(is_superuser=0).delete()

        self.stdout.write('Complete.')


