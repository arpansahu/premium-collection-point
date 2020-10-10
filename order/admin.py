from django.contrib import admin
from order.models import Order, moneyOrder

# Register your models here.
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(Order):
    # list_display = ('username',)
    search_fields = ('policyNumber', 'policyHolderName',)
    readonly_fields = ('date', 'lamount')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Order)
admin.site.register(moneyOrder)
