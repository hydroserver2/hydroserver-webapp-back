# Generated by Django 4.1.4 on 2023-01-17 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_thingownership'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='site',
            name='registration_date',
        ),
        migrations.DeleteModel(
            name='ThingOwnership',
        ),
    ]
