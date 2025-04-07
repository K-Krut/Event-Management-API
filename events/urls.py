from django.urls import path

from events.views import EventListView, EventMyListView, EventMyOrganizedListView

urlpatterns = [
    path('events/', EventListView.as_view(), name='events'),
    path('events/my/', EventMyListView.as_view(), name='events_my'),
    path('events/my/organized', EventMyOrganizedListView.as_view(), name='events_my_organized'),
]
