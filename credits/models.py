import math
from decimal import Decimal

from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator
from django.db.transaction import atomic

from datetime import timedelta

from common.models import *


class CreditType(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


name_validator = RegexValidator(regex=r'^1201\d{9}$', message='Значение типа 1201000000000')


class CreditProgram(models.Model):
    credit_type = models.ForeignKey(CreditType, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField('Duration in months')
    percent = models.FloatField('Percent', validators=[MinValueValidator(0.99), MaxValueValidator(100.0)])
    active = models.BooleanField(default=True)

    def __str__(self):
        return 'Кредит ({}) в {} на {} месяца(ев) под {} %'.format(
            self.credit_type.name, self.currency.code, self.duration, self.percent
        )


class CreditContract(models.Model):
    credit_program = models.ForeignKey(CreditProgram, on_delete=models.CASCADE)
    number = models.CharField('Number', max_length=9, editable=False, default=random_string)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateField('Start date')
    days_left = models.PositiveIntegerField('Days left')
    end_date = models.DateField('End date', blank=True, null=True)
    amount = models.DecimalField('Amount', max_digits=15, decimal_places=2)
    main_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='main_c')
    percent_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='percent_c')
    closed = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='credits', blank=True, null=True)

    def __str__(self):
        return self.number

    def close_day(self):
        self.days_left -= 1

        if self.credit_program.credit_type.name == 'Аннуитентный платеж':
            i = self.credit_program.percent / 100
            n = self.credit_program.duration
            k = (i * ((i + 1) ** n)) / (((1 + i) ** n) - 1)
            month_proceeds = self.amount * Decimal(k) - (self.amount / self.credit_program.duration)
            day_proceeds = month_proceeds / 30
        else:
            left_amount = self.amount / self.credit_program.duration * math.ceil((self.days_left + 1 )/ 30)
            day_proceeds = left_amount * Decimal(self.credit_program.percent / 100) / 30
        day_proceeds = round(day_proceeds, 2)

        bank_account = Account.objects.get(code='7327', currency=self.credit_program.currency)
        with atomic():
            self.percent_account.withdrawal(day_proceeds)
            bank_account.refill(day_proceeds)

        if (self.credit_program.duration * 30 - self.days_left) % 30 == 0:

            month_proceed_percent = - self.percent_account.balance
            cash_account = Account.objects.get(code='1010', currency=self.credit_program.currency)

            cash_account.refill(month_proceed_percent)
            with atomic():
                cash_account.withdrawal(month_proceed_percent)
                self.percent_account.refill(month_proceed_percent)

            month_proceed_main = self.amount / self.credit_program.duration

            cash_account.refill(month_proceed_main)
            with atomic():
                cash_account.withdrawal(month_proceed_main)
                self.main_account.refill(month_proceed_main)

            with atomic():
                self.main_account.withdrawal(month_proceed_main)
                bank_account.refill(month_proceed_main)

        if self.days_left == 0:
            self.end_date = self.start_date + timedelta(days=self.credit_program.duration * 30)
            self.closed = True

        self.save()
