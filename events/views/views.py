from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from events.decorators import server_exception
from events.models import Event
from events.views.mixins import EventListMixin


class EventListView(EventListMixin, generics.ListAPIView):

    @server_exception
    def get_queryset(self):
        return Event.objects.exclude(status__name__in=['Draft', 'Canceled']).order_by(*self.ordering)


class EventMyListView(EventListMixin, generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    @server_exception
    def get_queryset(self):
        return Event.objects.exclude(status__name__in=['Draft', 'Canceled']).filter(
            event__user=self.request.user).order_by(*self.ordering)


class EventMyOrganizedListView(EventListMixin, generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    @server_exception
    def get_queryset(self):
        return Event.objects.exclude(status__name__in=['Draft', 'Canceled']).filter(
            organizer=self.request.user).order_by(*self.ordering)
