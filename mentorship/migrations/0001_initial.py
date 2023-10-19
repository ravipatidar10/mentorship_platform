# Generated by Django 4.2.6 on 2023-10-18 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mentee', '0001_initial'),
        ('mentor', '0003_research_remove_mentor_research_area_researchdetails_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentorship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'pending'), (2, 'accepted'), (3, 'rejected')])),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentee.mentee')),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentor.mentor')),
                ('research', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentor.researchdetails')),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(1, 'completed'), (2, 'not_started'), (3, 'running')])),
                ('mentorship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship.mentorship')),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('time', models.DateTimeField()),
                ('mentorship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship.mentorship')),
            ],
        ),
    ]