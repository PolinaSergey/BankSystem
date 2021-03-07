import random

from django.db import models
from django.core import validators
from django.utils.timezone import now


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CivilCondition(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Disability(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Citizenship(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


name_validator = validators.RegexValidator(regex=r'^[a-zA-Zа-яА-Яё]*$', message='Field must contain only letters.')
num_validator = validators.RegexValidator(regex=r'\d{7}', message='Field must contain seven numbers.')
identity_validator = validators.RegexValidator(regex=r'^\d{7}[a-zA-Z]\d{3}[a-zA-Z]{2}\d$',
                                               message='Field must contain number like 0000000Z000ZZ0')
series_validator = validators.RegexValidator(regex=r'[A-Z]{2}',
                                             message='Field must contain two latin uppercase letters.')
phone_validator = validators.RegexValidator(regex=r'^[+]{1}[(]{0,1}[0-9]{1,5}[)]{0,1}[-\s\./0-9]*$',
                                            message='Field must contain phone number like +375000000000.')


class Client(models.Model):
    surname = models.CharField(max_length=100, validators=[name_validator])
    name = models.CharField(max_length=50, validators=[name_validator])
    mid_name = models.CharField(max_length=100, validators=[name_validator])

    date_of_birth = models.DateField('Birth date')

    passport_number = models.CharField(max_length=7, validators=[num_validator])
    passport_series = models.CharField(max_length=2, validators=[series_validator])
    issued_by = models.CharField(max_length=100)
    issued_on = models.DateField('issued on')
    identity_number = models.CharField(max_length=14, unique=True, validators=[identity_validator])

    birth_place = models.CharField(max_length=200)
    city_of_registration = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_of_registration')
    address_of_registration = models.CharField(max_length=50)
    current_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='current_city')
    current_address = models.CharField(max_length=50)
    phone_home = models.CharField(max_length=15, null=True, blank=True, validators=[phone_validator])
    phone_mobile = models.CharField(max_length=15, null=True, blank=True, validators=[phone_validator])
    email = models.EmailField(null=True, blank=True)
    work_place = models.CharField(max_length=200, null=True, blank=True)
    occupation = models.CharField(max_length=200, null=True, blank=True)
    monthly_income = models.FloatField(null=True, blank=True)

    civil_condition = models.ForeignKey(CivilCondition, on_delete=models.CASCADE)
    citizenship = models.ForeignKey(Citizenship, on_delete=models.CASCADE)
    disability = models.ForeignKey(Disability, on_delete=models.CASCADE)
    retiree = models.BooleanField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['passport_series', 'passport_number'], name='unique_client_passport')]

    def __str__(self):
        return f'{self.surname} {self.name} {self.mid_name} {self.passport_series.upper()}{self.passport_number}'

    def get_passport(self):
        return self.passport_series + self.passport_number


class Currency(models.Model):
    name = models.CharField(max_length=25)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.code.upper()


def random_string():
    return str(random.randint(1, 999999999)).rjust(9, '0')


class Account(models.Model):
    suffix_number = models.CharField('Number suffix', max_length=9, editable=False, default=random_string)
    code = models.CharField(
        'Code', max_length=4,  editable=False, choices=(
            ('3014', '3014'), ('2400', '2400'), ('1010', '1010'), ('7327', ' 7327')
        ),
    )
    activity = models.CharField(
        'Activity', max_length=255, choices=(
            ('active', 'active'), ('passive', 'passive'), ('active-passive', 'active-passive')
        )
    )
    debit = models.DecimalField('Debit', max_digits=15, decimal_places=2)
    credit = models.DecimalField('Credit', max_digits=15, decimal_places=2)
    balance = models.DecimalField('Balance', max_digits=15, decimal_places=2)
    name = models.CharField('Name', max_length=256)
    description = models.TextField('Description', blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, blank=True, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('code', 'suffix_number')

    @property
    def number(self):
        return self.code + self.suffix_number

    def __str__(self):
        return self.number

    def withdrawal(self, amount):
        if self.activity == 'active':
            self.credit += amount
            self.balance = self.debit - self.credit
            self.save()
        elif self.activity == 'passive':
            self.debit += amount
            self.balance = self.credit - self.debit
            self.save()

    def refill(self, amount):
        if self.activity == 'active':
            self.debit += amount
            self.balance = self.debit - self.credit
            self.save()
        elif self.activity == 'passive':
            self.credit += amount
            self.balance = self.credit - self.debit
            self.save()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        AccountLogs.objects.create(
            suffix_number=self.suffix_number,
            code=self.code,
            activity=self.activity,
            debit=self.debit,
            credit=self.credit,
            balance=self.balance,
            name=self.name,
            currency=self.currency,
            client_id=self.client_id
        )
        super(Account, self).save(force_insert, force_update, using, update_fields)


class AccountLogs(models.Model):
    created = models.DateTimeField(auto_now_add=now, editable=False)
    suffix_number = models.CharField('Number suffix', max_length=9, editable=False, default=random_string)
    code = models.CharField(
        'Code', max_length=4,  editable=False, choices=(
            ('3014', '3014'), ('2400', '2400'), ('1010', '1010'), ('7327', ' 7327')
        ),
    )
    activity = models.CharField(
        'Activity', max_length=255, choices=(
            ('active', 'active'), ('passive', 'passive'), ('active-passive', 'active-passive')
        )
    )
    debit = models.DecimalField('Debit', max_digits=15, decimal_places=2)
    credit = models.DecimalField('Credit', max_digits=15, decimal_places=2)
    balance = models.DecimalField('Balance', max_digits=15, decimal_places=2)
    name = models.CharField('Name', max_length=256)
    description = models.TextField('Description', blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, blank=True, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('created', 'code', 'suffix_number')

