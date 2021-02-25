# Generated by Django 3.1.5 on 2021-02-16 10:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inspection', '0023_inspectionentity_inspectors'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inspection',
            old_name='start_datetime',
            new_name='start_date_time',
        ),
        migrations.RemoveField(
            model_name='inspection',
            name='device',
        ),
        migrations.RemoveField(
            model_name='inspection',
            name='inspector',
        ),
        migrations.RemoveField(
            model_name='inspection',
            name='pdf',
        ),
        migrations.RemoveField(
            model_name='inspection',
            name='status',
        ),
        migrations.RemoveField(
            model_name='inspection',
            name='title',
        ),
        migrations.RemoveField(
            model_name='inspectionentity',
            name='inspectors',
        ),
        migrations.AddField(
            model_name='inspection',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inspection_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inspection',
            name='devices',
            field=models.ManyToManyField(related_name='inspection', to='inspection.Device'),
        ),
        migrations.AddField(
            model_name='inspection',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inspection', to='inspection.inspectionentity'),
        ),
        migrations.AddField(
            model_name='inspection',
            name='inspection_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inspection', to='inspection.inspectiontype'),
        ),
        migrations.AddField(
            model_name='inspection',
            name='inspectors',
            field=models.ManyToManyField(related_name='inspection_inspectors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inspection',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='DeviceInspection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('start_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('pdf', models.FileField(blank=True, null=True, upload_to='inspection/pdfs/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('status', models.CharField(choices=[('ready_to_start', 'Ready to start'), ('in_progress', 'In progress'), ('complete', 'Complete')], default='ready_to_start', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_inspection', to='inspection.device')),
                ('inspector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='device_inspection', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]