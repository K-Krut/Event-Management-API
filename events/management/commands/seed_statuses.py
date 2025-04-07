from django.core.management.base import BaseCommand

from events.constants import EVENT_STATUSES
from events.models import EventStatus


class Command(BaseCommand):
    help = 'Seed data for EventStatuses Model'

    def handle(self, *args, **kwargs):

        for status_name in EVENT_STATUSES:
            EventStatus.objects.create(
                name=status_name
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated data entries'))
