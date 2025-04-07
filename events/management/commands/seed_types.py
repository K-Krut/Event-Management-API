from django.core.management.base import BaseCommand

from events.constants import EVENT_TYPES
from events.models import EventType


class Command(BaseCommand):
    help = 'Seed data for EventTypes Model'

    def handle(self, *args, **kwargs):
        for event_type in EVENT_TYPES:
            EventType.objects.create(
                name=event_type
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated data entries'))
