from django.core.management.base import BaseCommand
from django.db.models import Count

from events.models import Event, EventParticipants
import random
from users.models import User


class Command(BaseCommand):
    help = 'Generate fake data for EventParticipants Model'

    def handle(self, *args, **kwargs):

        events = Event.objects.all()  # events = Event.objects.annotate(participant_count=Count('event')).filter(participant_count__lt=2)
        users = User.objects.filter(is_active=True)
        maximum_possible_participants = len(users) - 1

        for event in events:
            possible_participants = list(users.exclude(id=event.organizer.id))
            number_of_participants = random.randint(1, maximum_possible_participants)
            participants = random.sample(possible_participants, number_of_participants)
            for participant in participants:
                EventParticipants.objects.create(
                    event=event,
                    user=participant
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated fake data entries'))