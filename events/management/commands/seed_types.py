from django.core.management.base import BaseCommand
from events.models import EventType

event_types_data = [
    "Conference", "Meetup", "Webinar", "Hackathon", "Lecture", "Networking", "Exhibition"
]


class Command(BaseCommand):
    help = 'Seed data for EventTypes Model'

    def handle(self, *args, **kwargs):
        for status_name in event_types_data:
            EventType.objects.create(
                name=status_name
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated data entries'))
