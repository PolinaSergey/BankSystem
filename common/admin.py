from django.contrib import admin
from .models import *


class ClientAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'mid_name', 'date_of_birth', 'get_passport', 'issued_on', 'issued_by',
                    'identity_number', 'birth_place', 'city_of_registration', 'current_city', 'current_address',
                    'phone_home', 'phone_mobile', 'email', 'work_place', 'occupation', 'monthly_income',
                    'civil_condition', 'citizenship', 'disability', 'retiree')


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'activity', 'debit', 'credit', 'balance', 'currency',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AccountLogsAdmin(admin.ModelAdmin):
    list_display = ('created', 'name', 'code', 'activity', 'debit', 'credit', 'balance', 'currency',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Client, ClientAdmin)
admin.site.register(City)
admin.site.register(Disability)
admin.site.register(CivilCondition)
admin.site.register(Citizenship)
admin.site.register(Currency)
admin.site.register(Account, AccountAdmin)
admin.site.register(AccountLogs, AccountLogsAdmin)
