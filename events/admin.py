from import_export import resources
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from .models import RiderProfile, Event, Profile, Codes, Merchandise, MerchandiseOrder, ClubEvent, SignupPromotion
from .forms import RiderClass
from import_export.fields import Field

admin.site.site_header = 'Lobos Events/ User Database'
admin.site.register(Event)


class RiderProfileResource(resources.ModelResource):
    class Meta:
        model = RiderProfile
        # fields = ('last_name', 'first_name', 'riding_together', 'rider_class', 'address', 'city', 'state', 'zip_code',
        #           'phone_number', 'email', 'mach', 'emergency_contact_name', 'emergency_contact_phone', 'birth_date')
        # export_order = fields


# @admin.register(RiderProfile)
class RiderProfileExportAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = RiderProfileResource
    exclude = ['email2']
    list_display = ('first_name', 'last_name', 'email', 'event', 'confirmation_number', 'registration_date_time')
    search_fields = ('event__event_name', 'confirmation_number', 'first_name', 'last_name', 'email',)


admin.site.register(RiderProfile, RiderProfileExportAdmin)


@admin.register(Codes)
class CodesExportAdmin(ImportExportModelAdmin):
    list_display = ('discount_code', 'discount_amount')
    search_fields = ('discount_code', 'discount_amount')

    def user_info(self, obj):
        return obj.description


@admin.register(SignupPromotion)
class SignupPromotionAdmin(ImportExportModelAdmin):
    list_display = ('promotion_item_name', 'promotion_limit', 'promotion_classes', 'promotion_options')
    search_fields = ('promotion_item_name', 'promotion_limit', 'promotion_classes', 'promotion_options')
    form = RiderClass

    def user_info(self, obj):
        return obj.description


@admin.register(ClubEvent)
# this is the example of how to setup the import/ export and the admin search
class ClubEventExportAdmin(ImportExportModelAdmin):
    list_display = ('name', 'riderClass')
    search_fields = ('name', 'riderClass')

    def user_info(self, obj):
        return obj.description


@admin.register(MerchandiseOrder)
# this is the example of how to setup the import/ export and the admin search
class MerchandiseOrderExportAdmin(ImportExportModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'paypal_order_id', 'date_ordered', 'date_shipped', 'shipped')
    search_fields = ('first_name', 'last_name', 'email', 'paypal_order_id', 'date_ordered', 'date_shipped', 'shipped',)

    def user_info(self, obj):
        return obj.description


@admin.register(Merchandise)
# this is the example of how to setup the import/ export and the admin search
class MerchandiseExportAdmin(ImportExportModelAdmin):
    list_display = ('merchandise_name', 'sale_price', 'description', 'available_on_merch_page')
    search_fields = ('merchandise_name', 'sale_price', 'description', 'available_on_merch_page',)

    def user_info(self, obj):
        return obj.description


@admin.register(Profile)
# this is the example of how to setup the import/ export and the admin search
class ProfileExportAdmin(ImportExportModelAdmin):
    list_display = ('user', 'phone_number', 'birth_date')
    search_fields = ('phone_number', 'birth_date')

    def user_info(self, obj):
        return obj.description


class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)
