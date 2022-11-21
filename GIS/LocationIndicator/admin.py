from django.contrib import admin
from .models import Points


class LocationIndicatorAdmin(admin.ModelAdmin):
    list_filter = (
        "name",
        "location"
    )
    list_display = (
        "name",
        "location",
        "description"
    )
    search_fields = (
        "name",
        "description"
    )


admin.site.register(Points)