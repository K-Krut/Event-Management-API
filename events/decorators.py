from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from functools import wraps


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
