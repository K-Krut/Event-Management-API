from django.urls import path

from events.views import EventListView

urlpatterns = [
    path('events/', EventListView.as_view(), name='events'),
]