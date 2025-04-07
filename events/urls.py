from django.urls import path

from events.views.views import EventListView, EventMyListView, EventMyOrganizedListView, EventCreateView

urlpatterns = [
    path('events/', EventListView.as_view(), name='events'),
    path('events/create/', EventCreateView.as_view(), name='events'),
    path('events/my/', EventMyListView.as_view(), name='events_my'),
    path('events/my/organized', EventMyOrganizedListView.as_view(), name='events_my_organized'),
]
