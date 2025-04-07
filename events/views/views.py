from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from events.models import Event
from events.serializers import EventSerializer
from events.views.mixins import EventListMixin


class EventListView(EventListMixin, generics.ListAPIView):

    def get_queryset(self):
        try:
            return Event.objects.exclude(status__name__in=['Draft', 'Canceled']).order_by(*self.ordering)
        except Exception as error:
            return Response({'errors': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventMyListView(EventListMixin, generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            return Event.objects.exclude(status__name__in=['Draft', 'Canceled']).filter(
                event__user=self.request.user).order_by(*self.ordering)
        except Exception as error:
            return Response({'errors': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventMyOrganizedListView(EventListMixin, generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            return Event.objects.exclude(status__name__in=['Draft', 'Canceled']).filter(
                organizer=self.request.user).order_by(*self.ordering)
        except Exception as error:
            return Response({'errors': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
