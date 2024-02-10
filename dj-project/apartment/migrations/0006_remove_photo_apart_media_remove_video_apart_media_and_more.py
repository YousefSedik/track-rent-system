# Generated by Django 5.0.1 on 2024-02-08 16:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0005_apartment_public_visibility'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='apart_media',
        ),
        migrations.RemoveField(
            model_name='video',
            name='apart_media',
        ),
        migrations.AddField(
            model_name='photo',
            name='apartment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='apartment.apartment'),
        ),
        migrations.AddField(
            model_name='video',
            name='apartment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='apartment.apartment'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(null=True, upload_to='photos/'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(null=True, upload_to='videos/'),
        ),
        migrations.DeleteModel(
            name='ApartmentMedia',
        ),
    ]
