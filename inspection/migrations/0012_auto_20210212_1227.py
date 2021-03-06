# Generated by Django 3.1.5 on 2021-02-12 12:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inspection', '0011_auto_20210212_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspectiontype',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inspectiontype',
            name='reated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inspection_type', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inspectiontype',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
