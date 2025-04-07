from rest_framework import serializers

from events.models import Event, EventParticipants


class EventSerializer(serializers.ModelSerializer):
    is_registered = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'date_start', 'date_end', 'status', 'is_registered']

    def get_is_registered(self, obj):
        user = self.context['request'].user

        return False if not user.is_authenticated else EventParticipants.objects.filter(user=user, event=obj).exists()

