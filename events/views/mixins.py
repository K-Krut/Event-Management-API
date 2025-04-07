from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from events.serializers import EventSerializer


class Pagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100


class EventListMixin:
    serializer_class = EventSerializer

    pagination_class = Pagination
    ordering_fields = ['title', 'date_start', 'date_end', 'status']
    ordering = ['date_start', 'status']

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
