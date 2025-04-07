from django.db import models


class EventType(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name



class EventStatus(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name
