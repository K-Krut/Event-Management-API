from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from functools import wraps

from events.models import Event


def server_exception(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as error:
            return Response({'errors': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return wrapper


def event_exceptions(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({'errors': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        except TimeoutError:
            return Response({'errors': 'Request timeout'}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        except Exception as error:
            return Response({'errors': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return wrapper


def organizer_required(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        event_id = kwargs.get('id')
        event = Event.objects.get(id=event_id)
        if event.organizer != request.user:
            return Response({'errors': 'Access forbidden'}, status=status.HTTP_403_FORBIDDEN)

        self.event = event
        return func(self, request, *args, **kwargs)

    return wrapper
