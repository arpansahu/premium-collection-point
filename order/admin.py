from django.contrib import admin
from order.models import Order, Moneyorder

# Register your models here.
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(Order):
    # list_display = ('username',)
    search_fields = ('policy_number', 'policy_holder_name',)
    readonly_fields = ('date', 'lamount')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Order)
admin.site.register(Moneyorder)
