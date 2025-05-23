import logging
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from functools import wraps

from events.constants import EVENT_STATUSES_NOT_EDITABLE, EVENT_STATUSES_ACTIVE
from events.models import Event, EventParticipants

logger = logging.getLogger(__name__)


def server_exception(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as error:
            logger.error(f"----#ERROR in {self.__class__.__name__}.{func.__name__}\n{str(error)}")
            return Response({'errors': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return wrapper


def obj_exceptions(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except ObjectDoesNotExist:
            logger.error(f"----#ERROR in {self.__class__.__name__}.{func.__name__}\nObjectDoesNotExist")
            return Response({'errors': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        except TimeoutError:
            logger.error(f"----#ERROR in {self.__class__.__name__}.{func.__name__}\nTimeoutError")
            return Response({'errors': 'Request timeout'}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        except Exception as error:
            logger.error(f"----#ERROR in {self.__class__.__name__}.{func.__name__}\n{str(error)}")
            return Response({'errors': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return wrapper


def organizer_required(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        event_id = kwargs.get('id')
        event = Event.objects.get(id=event_id)
        if event.organizer != request.user:
            logger.error(f"----#ERROR in {self.__class__.__name__}.{func.__name__}\nAccess forbidden")
            return Response({'errors': 'Access forbidden'}, status=status.HTTP_403_FORBIDDEN)

        self.event = event
        return func(self, request, *args, **kwargs)

    return wrapper


def event_editable(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        if self.event.status.name in EVENT_STATUSES_NOT_EDITABLE:
            logger.error(f"----#ERROR in {self.__class__.__name__}.{func.__name__}\nFinished Events can\'t be updated")
            return Response({'errors': 'Finished Events can\'t be updated'}, status=status.HTTP_400_BAD_REQUEST)

        return func(self, request, *args, **kwargs)

    return wrapper


def event_deletable(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        if self.event.status.name in EVENT_STATUSES_NOT_EDITABLE:
            logger.error(f"----#ERROR in {self.__class__.__name__}.{func.__name__}\nFinished Events can\'t be deleted")
            return Response({'errors': 'Finished Events can\'t be deleted'}, status=status.HTTP_400_BAD_REQUEST)

        participants = EventParticipants.objects.filter(event=self.event).exclude(user=self.event.organizer).exists()

        if self.event.status.name in EVENT_STATUSES_ACTIVE and participants:
            logger.error(f"----#ERROR in {self.__class__.__name__}.{func.__name__}\n"
                         f"Active event with registered users can\'t be deleted")
            return Response({'errors': 'Active event with registered users can\'t be deleted'},
                            status=status.HTTP_400_BAD_REQUEST)

        return func(self, request, *args, **kwargs)

    return wrapper
