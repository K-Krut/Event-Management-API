from django.contrib import admin

from events.models import EventParticipants, Event, EventStatus, EventType, EventFormat


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(EventStatus)
class EventStatusAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(EventFormat)
class EventFormatAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'date_start', 'date_end', 'location', 'status', 'type', 'format',
        'organizer', 'created_at'
    ]
    list_filter = ['status', 'type', 'format', 'date_start', 'date_end']
    search_fields = ['title', 'description']
    ordering = ['status', 'date_start', 'type', 'created_at']
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(EventParticipants)
class EventParticipantsAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'registered_at']
    list_filter = ['event', 'user']
    search_fields = ['event__title', 'user__email']
    autocomplete_fields = ['event', 'user']
    ordering = ['-registered_at']
    show_facets = admin.ShowFacets.ALWAYS