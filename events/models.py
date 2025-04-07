from django.db import models

from users.models import User


class EventType(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name


class EventStatus(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name


class EventFormat(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.ForeignKey(EventStatus, on_delete=models.PROTECT,  related_name='events')
    format = models.ForeignKey(EventFormat, on_delete=models.PROTECT,  related_name='events')
    type = models.ForeignKey(EventType, on_delete=models.PROTECT,  related_name='events')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organizer')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_start']
        indexes = [
            models.Index(fields=['-date_start']),
        ]

    def __str__(self):
        return self.title


class EventParticipants(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-registered_at']
        unique_together = ('event', 'user')

    def __str__(self):
        return f'{self.event.title} - {self.user.first_name} {self.user.last_name}'
