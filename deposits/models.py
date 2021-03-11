from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator
from django.db.transaction import atomic


from datetime import datetime,timedelta

from common.models import *


class DepositType(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


name_validator = RegexValidator(regex=r'^1201\d{9}$', message='Значение типа 1201000000000')


class DepositProgram(models.Model):
    deposit_type = models.ForeignKey(DepositType, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField('Duration in months')
    percent = models.FloatField('Percent', validators=[MinValueValidator(0.99), MaxValueValidator(100.0)])
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{} вклад в {} на {} месяца(ев) под {} %'.format(
            self.deposit_type.name, self.currency.code, self.duration, self.percent
        )


class DepositContract(models.Model):
    deposit_program = models.ForeignKey(DepositProgram, on_delete=models.CASCADE)
    number = models.CharField('Number', max_length=9, editable=False, default=random_string)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateField('Start date')
    days_left = models.PositiveIntegerField('Days left')
    end_date = models.DateField('End date', blank=True, null=True)
    amount = models.DecimalField('Amount', max_digits=15, decimal_places=2)
    main_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='main')
    percent_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='percent')
    closed = models.BooleanField(default=False)

    def close_day(self):
        self.days_left -= 1

        day_percent = self.deposit_program.percent / 30
        day_proceeds = self.main_account.credit * Decimal(day_percent) / 100
        bank_account = Account.objects.get(code='7327', currency=self.deposit_program.currency)
        with atomic():
            bank_account.withdrawal(day_proceeds)
            self.percent_account.refill(day_proceeds)

        if (self.deposit_program.duration * 30 - self.days_left) % 30 == 0 and \
                self.days_left != 0 and \
                self.deposit_program.deposit_type.name != 'Безотзывный':
            month_proceed = self.percent_account.balance
            cash_account = Account.objects.get(code='1010', currency=self.deposit_program.currency)

            with atomic():
                self.percent_account.withdrawal(self.percent_account.balance)
                cash_account.refill(month_proceed)

            cash_account.withdrawal(month_proceed)

        if self.days_left == 0:
            self.close()
        else:
            self.save()

    def close(self):
        bank_account = Account.objects.get(code='7327', currency=self.deposit_program.currency)
        deposit_balance = self.main_account.credit
        with atomic():
            bank_account.withdrawal(deposit_balance)
            self.main_account.refill(deposit_balance)

        cash_account = Account.objects.get(code='1010', currency=self.deposit_program.currency)
        with atomic():
            self.main_account.withdrawal(deposit_balance)
            cash_account.refill(deposit_balance)

        cash_account.withdrawal(deposit_balance)

        month_proceed = self.percent_account.balance
        cash_account = Account.objects.get(code='1010', currency=self.deposit_program.currency)

        with atomic():
            self.percent_account.withdrawal(self.percent_account.balance)
            cash_account.refill(month_proceed)

        cash_account.withdrawal(month_proceed)

        self.end_date = self.start_date + timedelta(days=(self.deposit_program.duration * 30) - self.days_left)
        self.closed = True
        self.save()
