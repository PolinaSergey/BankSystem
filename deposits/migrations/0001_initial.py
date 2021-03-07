# Generated by Django 3.0.2 on 2020-02-11 12:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('code', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='DepositType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('start_date', models.DateField()),
                ('duration', models.PositiveIntegerField(blank=True, default=0)),
                ('days_gone', models.PositiveIntegerField(blank=True, default=0)),
                ('start_balance', models.FloatField(validators=[django.core.validators.MinValueValidator(0.99)])),
                ('current_balance', models.FloatField(blank=True, default=0.0)),
                ('percent', models.FloatField(validators=[django.core.validators.MinValueValidator(0.99)])),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.Client')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deposits.Currency')),
                ('deposit_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deposits.DepositType')),
            ],
        ),
    ]
