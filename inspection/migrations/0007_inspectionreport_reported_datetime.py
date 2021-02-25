# Generated by Django 3.1.5 on 2021-02-05 21:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0006_inspection_start_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspectionreport',
            name='reported_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
