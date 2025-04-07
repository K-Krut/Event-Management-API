from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import datetime, timedelta

from events.models import Event, EventParticipants, EventStatus, EventType, EventFormat
from users.models import User

fake = Faker()


def random_dates_within_month(year, month):
    end_date = datetime(year + 1, 1, 1) - timedelta(days=1) if month == 12 \
        else datetime(year, month + 1, 1) - timedelta(days=1)
    start = fake.date_between_dates(datetime(year, month, 1), end_date.date())
    end = start + timedelta(days=random.choice([3, 4, 5, 7]))
    return start, end


class Command(BaseCommand):
    help = 'Generate fake data for Event Model'

    def add_arguments(self, parser):
        parser.add_argument('num_entries', type=int, help='Number of fake entries to generate')

    def handle(self, *args, **kwargs):
        num_entries = kwargs['num_entries']

        statuses = EventStatus.objects.all()
        types = EventType.objects.all()
        formats = EventFormat.objects.all()

        for _ in range(num_entries):
            event_format = random.choice(formats)
            dates = random_dates_within_month(2025, 4)
            location = None if event_format.name == "Online" else fake.address()
            organizer = random.choice(User.objects.all())

            event = Event.objects.create(
                title=fake.paragraph(1),
                description=fake.paragraph(random.randint(4, 15)),
                date_start=dates[0],
                date_end=dates[1],
                location=location,
                status=random.choice(statuses),
                format=event_format,
                type=random.choice(types),
                organizer=organizer
            )

            EventParticipants.objects.create(
                event=event,
                user=organizer
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {num_entries} fake data entries'))
