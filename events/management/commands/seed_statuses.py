from django.core.management.base import BaseCommand
from events.models import EventStatus


statuses_data = ['Draft', 'Active', 'Upcoming', 'Ongoing', 'Canceled', 'Finished']


class Command(BaseCommand):
    help = 'Seed data for EventStatuses Model'

    def handle(self, *args, **kwargs):

        for status_name in statuses_data:
            EventStatus.objects.create(
                name=status_name
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated data entries'))
