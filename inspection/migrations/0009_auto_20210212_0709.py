# Generated by Django 3.1.5 on 2021-02-12 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0008_auto_20210211_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='help_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
