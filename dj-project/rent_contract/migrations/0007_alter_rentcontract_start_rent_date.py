# Generated by Django 3.2.7 on 2024-02-21 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent_contract', '0006_auto_20240221_0213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentcontract',
            name='start_rent_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
