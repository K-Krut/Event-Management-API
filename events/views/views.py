from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from events.constants import EVENT_STATUSES_EXCLUDED_IN_LIST
from events.decorators import server_exception
from events.models import Event, EventParticipants
from events.serializers import EventCreateSerializer
from events.views.mixins import EventListMixin


class EventListView(EventListMixin, generics.ListAPIView):

    @server_exception
    def get_queryset(self):
        return Event.objects.exclude(status__name__in=EVENT_STATUSES_EXCLUDED_IN_LIST).order_by(*self.ordering)


class EventMyListView(EventListMixin, generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    @server_exception
    def get_queryset(self):
        return Event.objects.exclude(status__name__in=EVENT_STATUSES_EXCLUDED_IN_LIST).filter(
            event__user=self.request.user).order_by(*self.ordering)


class EventMyOrganizedListView(EventListMixin, generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    @server_exception
    def get_queryset(self):
        return Event.objects.exclude(status__name__in=EVENT_STATUSES_EXCLUDED_IN_LIST).filter(
            organizer=self.request.user).order_by(*self.ordering)


class EventCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventCreateSerializer

    @server_exception
    def perform_create(self, serializer):
        user = self.request.user
        event = serializer.save(organizer=user)
        EventParticipants.objects.create(event=event, user=user)
        # response = EventSerializer(event, context={'request': self.request})
        return Response(event, status=status.HTTP_201_CREATED)