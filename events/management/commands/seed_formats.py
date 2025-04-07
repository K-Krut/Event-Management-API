from django.core.management.base import BaseCommand
from events.models import EventFormat


formats_data = ["Online", "Offline", "Hybrid",]


class Command(BaseCommand):
    help = 'Seed data for EventFormats Model'

    def handle(self, *args, **kwargs):
        for event_format in formats_data:
            EventFormat.objects.create(
                name=event_format
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated data entries'))
