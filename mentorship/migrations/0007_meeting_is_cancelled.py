# Generated by Django 4.2.6 on 2023-11-17 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship', '0006_meeting_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='is_cancelled',
            field=models.BooleanField(default=False),
        ),
    ]
