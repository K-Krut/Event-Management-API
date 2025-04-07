from django.core.management.base import BaseCommand

from events.constants import EVENT_FORMATS
from events.models import EventFormat


class Command(BaseCommand):
    help = 'Seed data for EventFormats Model'

    def handle(self, *args, **kwargs):
        for event_format in EVENT_FORMATS:
            EventFormat.objects.create(
                name=event_format
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated data entries'))
