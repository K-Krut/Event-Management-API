from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from events.constants import EVENT_STATUSES_EXCLUDED_IN_LIST
from events.decorators import server_exception
from events.models import Event
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
