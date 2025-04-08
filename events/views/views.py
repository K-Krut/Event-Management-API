from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from events.constants import EVENT_STATUSES_EXCLUDED_IN_LIST
from events.decorators import server_exception, obj_exceptions, organizer_required, event_editable
from events.models import Event, EventParticipants, EventStatus, EventType, EventFormat
from events.serializers import EventCreateSerializer, EventDetailsSerializer, ParticipantSerializer, \
    EventParticipantSerializer, EventUpdateSerializer, EventStatusSerializer, EventFormatSerializer, EventTypeSerializer
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
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save(organizer=request.user)

        EventParticipants.objects.create(event=event, user=request.user)
        return Response(EventDetailsSerializer(event, context={'request': request}).data, status=status.HTTP_201_CREATED)


class EventDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventDetailsSerializer

    @obj_exceptions
    def get(self, request, *args, **kwargs):
        event_id = kwargs.get('id')
        event = Event.objects.get(id=event_id)
        response = self.serializer_class(event, context={'request': request})
        return Response(response.data, status=status.HTTP_200_OK)

    @obj_exceptions
    @organizer_required
    @event_editable
    def put(self, request, *args, **kwargs):
        serializer = EventCreateSerializer(self.event, data=request.data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        event = serializer.save()
        response = self.serializer_class(event, context={'request': request})
        return Response(response.data, status=status.HTTP_200_OK)

    @obj_exceptions
    @organizer_required
    @event_editable
    def patch(self, request, *args, **kwargs):
        serializer = EventUpdateSerializer(self.event, data=request.data, partial=True)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        event = serializer.save()
        response = self.serializer_class(event, context={'request': request})
        return Response(response.data, status=status.HTTP_200_OK)

    @obj_exceptions
    @organizer_required
    @event_deletable
    def delete(self, request, *args, **kwargs):
        self.event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventParticipantsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination
    serializer_class = EventParticipantSerializer

    @organizer_required
    @obj_exceptions
    def get(self, request, *args, **kwargs):
        participants = EventParticipants.objects.filter(event=self.event).exclude(user=self.event.organizer)

        return Response({
            'participants_number': participants.count(),
            'organizer': ParticipantSerializer(self.event.organizer).data,
            'participants': self.serializer_class(participants, many=True).data,

        }, status=status.HTTP_200_OK)


class EventStatusesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination
    serializer_class = EventStatusSerializer

    @server_exception
    def get_queryset(self):
        return EventStatus.objects.all()


class EventFormatsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination
    serializer_class = EventFormatSerializer

    @server_exception
    def get_queryset(self):
        return EventFormat.objects.all()


class EventTypesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination
    serializer_class = EventTypeSerializer

    @server_exception
    def get_queryset(self):
        return EventType.objects.all()
