# Generated by Django 3.1.5 on 2021-02-12 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0012_auto_20210212_1227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inspectiontype',
            old_name='reated_by',
            new_name='created_by',
        ),
    ]