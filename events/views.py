from rest_framework import generics, status, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from events.models import Event
from events.serializers import EventSerializer


class Pagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100


class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer

    pagination_class = Pagination
    ordering_fields = ['title', 'date_start', 'date_end', 'status']
    ordering = ['-date_start', 'status']

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']


    def get_queryset(self):
        try:
            return Event.objects.exclude(status__name__in=['Draft', 'Canceled']).order_by(*self.ordering)
        except Exception as error:
            return Response({'errors': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
