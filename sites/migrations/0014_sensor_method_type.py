# Generated by Django 4.1.4 on 2023-03-02 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0013_observation_valid_begin_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='method_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
