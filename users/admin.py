from django.contrib import admin
from django.utils import formats

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'first_name', 'last_name', 'email_notifications', 'formatted_registration_date', 'is_superuser',
        'is_staff', 'is_active'
    ]
    list_filter = ['email_notifications', 'created_at', 'is_superuser', 'is_staff', 'is_active']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['created_at', 'first_name', 'last_name']
    show_facets = admin.ShowFacets.ALWAYS

    def formatted_registration_date(self, obj):
        return formats.date_format(obj.created_at, "Y-m-d")

    formatted_registration_date.short_description = 'Registration Date'
