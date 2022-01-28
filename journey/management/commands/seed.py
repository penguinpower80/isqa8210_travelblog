from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django_seed import Seed
from faker.generator import random

from journey.models import Post, Comment


class Command(BaseCommand):
    help = "Seed database using Django Seed for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('Seeding Journey data...')
        seeder = Seed.seeder()

        # add some users
        user_count = random.randint(5, 25)

        User = get_user_model()

        all_users = User.objects.all()

        seeder.add_entity(User, user_count, {
            'username': lambda x: seeder.faker.unique.first_name() + '_' + seeder.faker.unique.last_name(),
            'is_staff': 0,
            'is_superuser': 0
        })
        inserted_user_pks = seeder.execute()
        self.stdout.write(str(user_count) + ' users added')

        uniq_image_ids = list(range(user_count * 25))  # max we can have
        random.shuffle(uniq_image_ids)

        all_users = User.objects.all()

        for i in inserted_user_pks[User]:
            self.stdout.write('For user ' + str(i) + ':')
            thisUser = User(i)
            min_journey = 4
            max_journey = 25
            random_journey_count = random.randint(min_journey, max_journey)
            self.stdout.write(' - Adding ' + str(random_journey_count) + ' journeys')
            seeder.add_entity(Post, random_journey_count, {
                'author': thisUser,
                'image_url': lambda x: "https://picsum.photos/640/480?img=" + str(uniq_image_ids.pop()),
            })
            inserted_post_pks = seeder.execute()
            for j in inserted_post_pks[Post]:
                self.stdout.write(' -- For journey ' + str(j) + ':')

                thisPost = Post(j)
                min_comment = 0
                max_comment = 10
                random_comment_count = random.randint(min_comment, max_comment)
                self.stdout.write(' ---- Adding ' + str(random_comment_count) + ' comments')
                if (random_comment_count > 0):
                    seeder.add_entity(Comment, random_comment_count, {
                        'post': thisPost,
                        'name': lambda x: random.choice(all_users)
                    })
