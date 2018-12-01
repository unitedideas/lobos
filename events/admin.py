from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import RiderProfile, Event, Profile, Codes

admin.site.site_header = 'Lobos Events/ User Database'
admin.site.register(Codes)
admin.site.register(Event)


@admin.register(RiderProfile)
# this is the example of how to setup the import/ export and the admin search
class RiderProfileExportAdmin(ImportExportModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'event', 'confirmation_number')
    search_fields = ('event__event_name', 'confirmation_number', 'first_name', 'last_name', 'email')

    def user_info(self, obj):
        return obj.description


@admin.register(Profile)
# this is the example of how to setup the import/ export and the admin search
class ProfileExportAdmin(ImportExportModelAdmin):
    list_display = ('user', 'phone_number', 'birth_date')
    search_fields = ('phone_number', 'birth_date')

    def user_info(self, obj):
        return obj.description


#
# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name_plural = 'Profile'
#     fk_name = 'user'
#
#
# class CustomUserAdmin(UserAdmin):
#     inlines = (ProfileInline,)
#     list_display = ('username', 'email', 'first_name', 'last_name')
#     list_select_related = ('profile',)
#
#     def get_inline_instances(self, request, obj=None):
#         if not obj:
#             return list()
#         return super(CustomUserAdmin, self).get_inline_instances(request, obj)


class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
