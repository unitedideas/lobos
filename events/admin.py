from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import RiderProfile, Event, Profile, Mail, MailText

admin.site.site_header = 'Lobos Events/ User Database'


#  attempt to add infor rows above the riderprofile  <, not working
class RiderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'event',)
    readonly_fields = ('registration_date_time',)
    search_fields = ("event__event_name", "event__event_date",)

    def user_info(self, obj):
        return obj.description


admin.site.register(RiderProfile, RiderProfileAdmin)
admin.site.register(Event)
admin.site.register(Profile)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_select_related = ('profile',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)



class MailAdmin(admin.ModelAdmin):
    model = Mail

admin.site.register(Mail)


class MailTextAdmin(admin.ModelAdmin):
    model = MailText


admin.site.register(MailText)
