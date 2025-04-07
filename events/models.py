from django.db import models

from users.models import User


class Type(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name



class Status(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    location = models.CharField(max_length=255)
    status = models.ForeignKey(Status, on_delete=models.PROTECT,  related_name='events')
    type = models.ForeignKey(Type, on_delete=models.PROTECT,  related_name='events')
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
