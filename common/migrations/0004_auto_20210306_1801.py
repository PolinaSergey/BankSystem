# Generated by Django 3.1.7 on 2021-03-06 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20210306_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='code',
            field=models.CharField(choices=[('3014', '3014'), ('2400', '2400'), ('1010', '1010'), ('7327', ' 7327')], editable=False, max_length=4, verbose_name='Code'),
        ),
    ]