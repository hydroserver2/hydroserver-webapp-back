# Generated by Django 4.2.4 on 2023-12-01 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_unitchangelog_thingchangelog_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='thing',
            name='hydroshare_archive_resource_id',
            field=models.CharField(blank=True, db_column='hydroshareArchiveResourceId', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='thingchangelog',
            name='hydroshare_archive_resource_id',
            field=models.CharField(blank=True, db_column='hydroshareArchiveResourceId', max_length=500, null=True),
        ),
    ]
