# Generated by Django 5.0.1 on 2024-03-20 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent_contract', '0010_alter_rentcontract_tenant_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentcontract',
            name='contract_photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/'),
        ),
    ]
