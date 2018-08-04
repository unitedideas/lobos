from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import RiderProfile, Event

admin.site.site_header = 'Lobos Events/ User Database'

#  attempt to add infor rows above the riderprofile  <, not working
class RiderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'event')

    def user_info(self, obj):
        return obj.description


admin.site.register(RiderProfile)
admin.site.register(Event)
