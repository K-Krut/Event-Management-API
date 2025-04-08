from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from events.constants import EVENT_STATUSES_ALLOWED_FOR_CREATE, EVENT_FORMATS_WITH_REQUIRED_LOCATION, \
    EVENT_FORMATS_WITHOUT_LOCATION
from events.models import Event, EventParticipants, EventStatus, EventType, EventFormat
from users.serializers import UserSerializer


class EventOptionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']


class EventStatusSerializer(EventOptionSerializer):
    class Meta(EventOptionSerializer.Meta):
        model = EventStatus


class EventFormatSerializer(EventOptionSerializer):
    class Meta(EventOptionSerializer.Meta):
        model = EventFormat


class EventTypeSerializer(EventOptionSerializer):
    class Meta(EventOptionSerializer.Meta):
        model = EventType


class ParticipantSerializer(UserSerializer):
    pass


class EventParticipantSerializer(serializers.ModelSerializer):
    user = ParticipantSerializer(read_only=True)

    class Meta:
        model = EventParticipants
        fields = ['user', 'registered_at']


class EventSerializer(serializers.ModelSerializer):
    is_registered = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'date_start', 'date_end', 'status', 'is_registered']

    def get_is_registered(self, obj):
        user = self.context['request'].user

        return False if not user.is_authenticated else EventParticipants.objects.filter(user=user, event=obj).exists()


class EventCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'date_start', 'date_end', 'location', 'status', 'format', 'type', 'organizer'
        ]
        read_only_fields = ['organizer', 'id']

    def validate_status(self, value):
        if value.name not in EVENT_STATUSES_ALLOWED_FOR_CREATE:
            raise ValidationError(f"Cant create event with {value.name} status")
        return value

    def validate(self, data):
        event_format = data.get('format', None)
        location = data.get('location', None)

        if not data.get('title'):
            raise ValidationError('title is required')

        if event_format.name in EVENT_FORMATS_WITH_REQUIRED_LOCATION and not location:
            raise ValidationError(f'location is required for {EVENT_FORMATS_WITH_REQUIRED_LOCATION} events')

        if event_format.name in EVENT_FORMATS_WITHOUT_LOCATION and location:
            raise ValidationError(f'location cant be added for {EVENT_FORMATS_WITHOUT_LOCATION} events')

        if not data['date_start'] < data['date_end']:
            raise ValidationError('Event\'s Date Start must be before Date End')

        return data


class EventDetailsSerializer(serializers.ModelSerializer):
    is_registered = serializers.SerializerMethodField()
    participants_number = serializers.SerializerMethodField()

    status = EventStatusSerializer(read_only=True)
    type = EventTypeSerializer(read_only=True)
    format = EventFormatSerializer(read_only=True)
    organizer = ParticipantSerializer(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'date_start', 'date_end', 'description', 'location', 'status', 'format', 'type',
            'is_registered', 'participants_number', 'organizer'
        ]

    def get_is_registered(self, obj):
        user = self.context['request'].user
        return False if not user.is_authenticated else EventParticipants.objects.filter(user=user, event=obj).exists()

    def get_participants_number(self, obj):
        return EventParticipants.objects.filter(event=obj).count()

