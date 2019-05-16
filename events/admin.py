from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import RiderProfile, Event, Profile, Codes, Merchandise, MerchandiseOrder

admin.site.site_header = 'Lobos Events/ User Database'
admin.site.register(Codes)
admin.site.register(Event)


@admin.register(MerchandiseOrder)
# this is the example of how to setup the import/ export and the admin search
class MerchandiseOrderExportAdmin(ImportExportModelAdmin):
    list_display = ('first_name', 'last_name', 'paypal_order_id', 'date_ordered', 'date_shipped', 'shipped')
    search_fields = ('first_name', 'last_name', 'paypal_order_id', 'date_ordered', 'date_shipped', 'shipped',)

    def user_info(self, obj):
        return obj.description


@admin.register(Merchandise)
# this is the example of how to setup the import/ export and the admin search
class MerchandiseExportAdmin(ImportExportModelAdmin):
    list_display = ('merchandise_name', 'sale_price', 'description', 'available_on_merch_page')
    search_fields = ('merchandise_name', 'sale_price', 'description', 'available_on_merch_page',)

    def user_info(self, obj):
        return obj.description


@admin.register(RiderProfile)
# this is the example of how to setup the import/ export and the admin search
class RiderProfileExportAdmin(ImportExportModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'event', 'confirmation_number', 'registration_date_time')
    search_fields = ('event__event_name', 'confirmation_number', 'first_name', 'last_name', 'email',)

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
