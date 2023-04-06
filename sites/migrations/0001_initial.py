# Generated by Django 4.1.5 on 2023-02-22 21:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Datastream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('unit_of_measurement', models.TextField()),
                ('observation_type', models.CharField(max_length=255)),
                ('properties', models.TextField(null=True)),
                ('observed_area', models.TextField(null=True)),
                ('phenomenon_time', models.DateTimeField(null=True)),
                ('result_time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeatureOfInterest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('encoding_type', models.CharField(max_length=255)),
                ('feature', models.TextField()),
                ('properties', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ObservedProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('definition', models.TextField()),
                ('description', models.TextField()),
                ('properties', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Thing',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('properties', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SensorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('manufacturer', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.CharField(blank=True, max_length=500, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('encoding_type', models.CharField(blank=True, max_length=255, null=True)),
                ('method_type', models.CharField(max_length=50, null=True)),
                ('method_link', models.CharField(blank=True, max_length=500, null=True)),
                ('method_code', models.CharField(blank=True, max_length=50, null=True)),
                ('sensor_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensors', to='sites.sensormodel')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('encoding_type', models.CharField(max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('elevation', models.FloatField()),
                ('city', models.CharField(blank=True, max_length=150, null=True)),
                ('state', models.CharField(blank=True, max_length=150, null=True)),
                ('country', models.CharField(blank=True, max_length=150, null=True)),
                ('properties', models.TextField(blank=True, null=True)),
                ('thing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='sites.thing')),
            ],
        ),
        migrations.AddField(
            model_name='datastream',
            name='observed_property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.observedproperty'),
        ),
        migrations.AddField(
            model_name='datastream',
            name='sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datastreams', to='sites.sensor'),
        ),
        migrations.AddField(
            model_name='datastream',
            name='thing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datastreams', to='sites.thing'),
        ),
        migrations.CreateModel(
            name='ThingAssociation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owns_thing', models.BooleanField(default=False)),
                ('follows_thing', models.BooleanField(default=False)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thing_associations', to=settings.AUTH_USER_MODEL)),
                ('thing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='associates', to='sites.thing')),
            ],
            options={
                'unique_together': {('thing', 'person')},
            },
        ),
    ]
