# Generated by Django 3.1.5 on 2021-02-13 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0015_auto_20210213_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='questioncategory',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_categories', to='inspection.inspectionentity'),
        ),
    ]
