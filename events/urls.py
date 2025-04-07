from django.urls import path

from events.views.views import EventListView, EventMyListView, EventMyOrganizedListView, EventCreateView, \
    EventDetailView

urlpatterns = [
    path('events/', EventListView.as_view(), name='events'),
    path('events/create/', EventCreateView.as_view(), name='events-create'),
    path('events/my/', EventMyListView.as_view(), name='events-my'),
    path('events/my/organized', EventMyOrganizedListView.as_view(), name='events-my-organized'),
    path('events/<int:id>/', EventDetailView.as_view(), name='event-details'),

]
