from django.urls import path

from events.views.views import EventListView, EventMyListView, EventMyOrganizedListView, EventCreateView, \
    EventDetailView, EventParticipantsView, EventStatusesView

urlpatterns = [
    path('events/', EventListView.as_view(), name='events'),
    path('events/create/', EventCreateView.as_view(), name='events-create'),
    path('events/my/', EventMyListView.as_view(), name='events-my'),
    path('events/my/organized', EventMyOrganizedListView.as_view(), name='events-my-organized'),
    path('events/<int:id>/', EventDetailView.as_view(), name='event-details'),
    path('events/<int:id>/participants/', EventParticipantsView.as_view(), name='event-participants'),
    path('events/statuses/', EventStatusesView.as_view(), name='events-statuses'),
    path('events/formats/', EventListView.as_view(), name='events-formats'),
    path('events/types/', EventListView.as_view(), name='events-types'),
]
