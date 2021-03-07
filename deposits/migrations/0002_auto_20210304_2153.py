# Generated by Django 3.1.7 on 2021-03-04 18:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposits', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='duration',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='Положительное целое число, 0 для депозита "До востребования"'),
        ),
        migrations.AlterField(
            model_name='deposit',
            name='name',
            field=models.CharField(help_text='Значение типа 1201000000000', max_length=20, unique=True, validators=[django.core.validators.RegexValidator(message='Значение типа 1201000000000', regex='^1201\\d{9}$')]),
        ),
        migrations.AlterField(
            model_name='deposit',
            name='percent',
            field=models.FloatField(help_text='Положительное число с разделителем точкой', validators=[django.core.validators.MinValueValidator(0.99)]),
        ),
        migrations.AlterField(
            model_name='deposit',
            name='start_balance',
            field=models.FloatField(help_text='Положительное число с разделителем точкой', validators=[django.core.validators.MinValueValidator(0.99)]),
        ),
    ]
