# Generated by Django 3.1.7 on 2021-03-06 13:25

import common.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Citizenship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CivilCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('code', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Disability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Field must contain only letters.', regex='^[a-zA-Zа-яА-Яё]*$')])),
                ('name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Field must contain only letters.', regex='^[a-zA-Zа-яА-Яё]*$')])),
                ('mid_name', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Field must contain only letters.', regex='^[a-zA-Zа-яА-Яё]*$')])),
                ('date_of_birth', models.DateField(verbose_name='Birth date')),
                ('passport_number', models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(message='Field must contain seven numbers.', regex='\\d{7}')])),
                ('passport_series', models.CharField(max_length=2, validators=[django.core.validators.RegexValidator(message='Field must contain two latin uppercase letters.', regex='[A-Z]{2}')])),
                ('issued_by', models.CharField(max_length=100)),
                ('issued_on', models.DateField(verbose_name='issued on')),
                ('identity_number', models.CharField(max_length=14, unique=True, validators=[django.core.validators.RegexValidator(message='Field must contain number like 0000000Z000ZZ0', regex='^\\d{7}[a-zA-Z]\\d{3}[a-zA-Z]{2}\\d$')])),
                ('birth_place', models.CharField(max_length=200)),
                ('address_of_registration', models.CharField(max_length=50)),
                ('current_address', models.CharField(max_length=50)),
                ('phone_home', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='Field must contain phone number like +375000000000.', regex='^[+]{1}[(]{0,1}[0-9]{1,5}[)]{0,1}[-\\s\\./0-9]*$')])),
                ('phone_mobile', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='Field must contain phone number like +375000000000.', regex='^[+]{1}[(]{0,1}[0-9]{1,5}[)]{0,1}[-\\s\\./0-9]*$')])),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('work_place', models.CharField(blank=True, max_length=200, null=True)),
                ('occupation', models.CharField(blank=True, max_length=200, null=True)),
                ('monthly_income', models.FloatField(blank=True, null=True)),
                ('retiree', models.BooleanField()),
                ('citizenship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.citizenship')),
                ('city_of_registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_of_registration', to='common.city')),
                ('civil_condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.civilcondition')),
                ('current_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_city', to='common.city')),
                ('disability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.disability')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suffix_number', models.CharField(default=common.models.random_string, editable=False, max_length=9, verbose_name='Number suffix')),
                ('code', models.CharField(choices=[('3014', '3014'), ('2400', '2400'), ('1010', '1010'), ('7327', ' 7327')], editable=False, max_length=4, verbose_name='Code')),
                ('activity', models.CharField(choices=[('active', 'active'), ('passive', 'passive'), ('active-passive', 'active-passive')], max_length=255, verbose_name='Activity')),
                ('debit', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Debit')),
                ('credit', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Credit')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Balance')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('client', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='common.client')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.currency')),
            ],
        ),
        migrations.AddConstraint(
            model_name='client',
            constraint=models.UniqueConstraint(fields=('passport_series', 'passport_number'), name='unique_client_passport'),
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together={('code', 'suffix_number')},
        ),


    ]
