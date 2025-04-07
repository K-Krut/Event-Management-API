import base64
import random

import requests
from django.core.management import BaseCommand
from faker import Faker

from users.models import User
from users.utils import convert_file

fake = Faker()


def get_random_avatar_base64():
    response = requests.get(f"https://i.pravatar.cc/{random.randint(100, 1000)}")
    if response.status_code == 200:
        encoded = base64.b64encode(response.content).decode('utf-8')
        return f"data:image/jpeg;base64,{encoded}"
    return None


class Command(BaseCommand):
    help = 'Seed Users'

    def add_arguments(self, parser):
        parser.add_argument('num', type=int)

    def handle(self, *args, **options):
        num = options['num']

        for _ in range(num):
            User.objects.create_user(
                email=fake.email(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                avatar=convert_file(get_random_avatar_base64())
            )
