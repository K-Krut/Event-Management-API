from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from events.constants import EVENT_STATUSES_EXCLUDED_IN_LIST
from events.decorators import server_exception, event_exceptions, organizer_required, event_editable
from events.models import Event, EventParticipants
from events.serializers import EventCreateSerializer, EventDetailsSerializer, ParticipantSerializer, \
    EventParticipantSerializer, EventUpdateSerializer
from events.views.mixins import EventListMixin, Pagination


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


class EventDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventDetailsSerializer

    @event_exceptions
    def get(self, request, *args, **kwargs):
        event_id = kwargs.get('id')
        event = Event.objects.get(id=event_id)
        response = self.serializer_class(event, context={'request': request})
        return Response(response.data, status=status.HTTP_200_OK)

    @event_exceptions
    @organizer_required
    @event_editable
    def put(self, request, *args, **kwargs):
        serializer = EventCreateSerializer(self.event, data=request.data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        event = serializer.save()
        response = self.serializer_class(event, context={'request': request})
        return Response(response.data, status=status.HTTP_200_OK)




class EventParticipantsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination
    serializer_class = EventParticipantSerializer

    @organizer_required
    @event_exceptions
    def get(self, request, *args, **kwargs):
        participants = EventParticipants.objects.filter(event=self.event).exclude(user=self.event.organizer)

        return Response({
            'participants_number': participants.count(),
            'organizer': ParticipantSerializer(self.event.organizer).data,
            'participants': self.serializer_class(participants, many=True).data,

        }, status=status.HTTP_200_OK)
