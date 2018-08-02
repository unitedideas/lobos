from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import RiderProfile, Event

admin.site.register(RiderProfile)
admin.site.register(Event)
