# Generated by Django 3.1.7 on 2021-03-06 13:57

from django.db import migrations, models


def add_system_account(apps, schema_editor):
    Account = apps.get_model("common", "Account")
    db_alias = schema_editor.connection.alias
    a = [
        Account(
            code="1010",
            activity="active",
            debit=0,
            credit=0,
            balance=0,
            name='Kacca BYN',
            currency_id=1,
            client=None,
        ),
        Account(
            code="1010",
            activity="active",
            debit=0,
            credit=0,
            balance=0,
            name='Kacca USD',
            currency_id=2,
            client=None,
        ),
        Account(
            code="1010",
            activity="active",
            debit=0,
            credit=0,
            balance=0,
            name='Kacca EUR',
            currency_id=3,
            client=None,
        ),
        Account(
            code="7327",
            activity="passive",
            debit=0,
            credit=1000000000,
            balance=1000000000,
            name='Фонд развития банка BYN',
            currency_id=1,
            client=None,
        ),
        Account(
            code="7327",
            activity="passive",
            debit=0,
            credit=1000000000,
            balance=1000000000,
            name='Фонд развития банка USD',
            currency_id=2,
            client=None,
        ),
        Account(
            code="7327",
            activity="passive",
            debit=0,
            credit=1000000000,
            balance=1000000000,
            name='Фонд развития банка EUR',
            currency_id=3,
            client=None,
        ),
    ]
    for i in a:
        i.save()


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20210306_1649'),
    ]

    operations = [
        migrations.RunPython(add_system_account, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='account',
            name='code',
            field=models.CharField(choices=[('3014', '3014'), ('2400', '2400')], editable=False, max_length=4, verbose_name='Code'),
        ),
    ]
