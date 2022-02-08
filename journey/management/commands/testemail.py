from django.core.mail import send_mail
from django.core.management import BaseCommand

# https://docs.djangoproject.com/en/4.0/topics/email/

class Command(BaseCommand):
    help = "Send Test Email."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('Sending Test Email...')
        send_mail(
            'Test from TravelBlog',
            'Here is the message.',
            'dhefley@unomaha.edu',
            ['dhefley@unomaha.edu'],
            fail_silently=False,
        )