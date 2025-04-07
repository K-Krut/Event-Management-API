from rest_framework import generics, status
from rest_framework.response import Response
from events.models import Event
from events.serializers import EventSerializer


class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        try:
            return Event.objects.all()
        except Exception as error:
            return Response({'errors': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
