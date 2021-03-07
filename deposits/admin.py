from django.contrib import admin
from django import forms


from .models import *


class DepositContractAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DepositContractAdminForm, self).__init__(*args, **kwargs)
        self.fields['deposit_program'].queryset = DepositProgram.objects.filter(active=True)

    class Meta:
        fields = ('deposit_program','client', 'start_date', 'amount')

    def save(self, commit=True):
        deposit = super(DepositContractAdminForm, self).save(commit=False)

        deposit.days_left = 30 * deposit.deposit_program.duration
        deposit.main_account = Account.objects.create(
            code="3014",
            activity="passive",
            debit=0,
            credit=0,
            balance=0,
            name='Основной по вкладу {}'.format(deposit.client),
            currency=deposit.deposit_program.currency,
            client=deposit.client,
        )
        deposit.percent_account = Account.objects.create(
            code="3014",
            activity="passive",
            debit=0,
            credit=0,
            balance=0,
            name='Процентный по вкладу {}'.format(deposit.client),
            currency=deposit.deposit_program.currency,
            client=deposit.client,
        )

        cash_account = Account.objects.get(code='1010', currency=deposit.deposit_program.currency)
        cash_account.refill(deposit.amount)

        with atomic():
            cash_account.withdrawal(deposit.amount)
            deposit.main_account.refill(deposit.amount)

        bank_account = Account.objects.get(code='7327', currency=deposit.deposit_program.currency)

        with atomic():
            deposit.main_account.withdrawal(deposit.amount)
            bank_account.refill(deposit.amount)

        return deposit


class DepositContractAdmin(admin.ModelAdmin):
    form = DepositContractAdminForm

    list_display = ('number', 'deposit_program', 'client', 'start_date', 'days_left', 'end_date',
                    'amount', 'main_account', 'percent_account', 'closed')

    actions = ['close_day', 'close']

    def close_day(self, request, queryset):
        for deposit_contr in queryset.filter(closed=False):
            deposit_contr.close_day()

    def close(self, request, queryset):
        for deposit_contr in queryset.filter(closed=False,
                                             deposit_program__deposit_type__name='Отзывный'):
            deposit_contr.close()


admin.site.register(DepositProgram)
admin.site.register(DepositContract, DepositContractAdmin)
admin.site.register(DepositType)
