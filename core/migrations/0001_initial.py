# Generated by Django 4.2.4 on 2023-08-25 22:17

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
            name='Observation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('result', models.FloatField()),
                ('result_time', models.DateTimeField()),
                ('result_quality', models.CharField(max_length=255, null=True)),
                ('phenomenon_time', models.DateTimeField(blank=True, null=True)),
                ('valid_begin_time', models.DateTimeField(blank=True, null=True)),
                ('valid_end_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DataLoader',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_loaders', to=settings.AUTH_USER_MODEL))

            ],
        ),
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('path', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('header_row', models.PositiveIntegerField(blank=True, null=True)),
                ('data_start_row', models.PositiveIntegerField(blank=True, null=True)),
                ('delimiter', models.CharField(blank=True, max_length=1, null=True)),
                ('quote_char', models.CharField(blank=True, max_length=1, null=True)),
                ('interval', models.PositiveIntegerField(blank=True, null=True)),
                ('interval_units', models.CharField(blank=True, max_length=255, null=True)),
                ('crontab', models.CharField(blank=True, max_length=255, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('paused', models.BooleanField()),
                ('timestamp_column', models.CharField(blank=True, max_length=255, null=True)),
                ('timestamp_format', models.CharField(blank=True, max_length=255, null=True)),
                ('timestamp_offset', models.CharField(blank=True, max_length=255, null=True)),
                ('data_source_thru', models.DateTimeField(blank=True, null=True)),
                ('last_sync_successful', models.BooleanField(blank=True, null=True)),
                ('last_sync_message', models.TextField(blank=True, null=True)),
                ('last_synced', models.DateTimeField(blank=True, null=True)),
                ('next_sync', models.DateTimeField(blank=True, null=True)),
                ('data_loader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.dataloader')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_sources', to=settings.AUTH_USER_MODEL))
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
            ],
        ),
        migrations.CreateModel(
            name='Thing',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('sampling_feature_type', models.CharField(blank=True, max_length=200, null=True)),
                ('sampling_feature_code', models.CharField(blank=True, max_length=200, null=True)),
                ('site_type', models.CharField(blank=True, max_length=200, null=True)),
                ('is_private', models.BooleanField(default=False)),
                ('include_data_disclaimer', models.BooleanField(default=False)),
                ('data_disclaimer', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('thing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='location', serialize=False, to='core.thing')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('encoding_type', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(decimal_places=16, max_digits=22)),
                ('longitude', models.DecimalField(decimal_places=16, max_digits=22)),
                ('elevation', models.DecimalField(decimal_places=16, max_digits=22)),
                ('elevation_datum', models.CharField(max_length=255)),
                ('city', models.CharField(blank=True, max_length=150, null=True)),
                ('state', models.CharField(blank=True, max_length=150, null=True)),
                ('county', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('symbol', models.CharField(max_length=255)),
                ('definition', models.TextField()),
                ('unit_type', models.CharField(max_length=255)),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('encoding_type', models.CharField(blank=True, max_length=255, null=True)),
                ('manufacturer', models.CharField(blank=True, max_length=255, null=True)),
                ('model', models.CharField(blank=True, max_length=255, null=True)),
                ('model_url', models.CharField(blank=True, max_length=500, null=True)),
                ('method_type', models.CharField(blank=True, max_length=100, null=True)),
                ('method_link', models.CharField(blank=True, max_length=500, null=True)),
                ('method_code', models.CharField(blank=True, max_length=50, null=True)),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProcessingLevel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('processing_level_code', models.CharField(max_length=255)),
                ('definition', models.TextField()),
                ('explanation', models.TextField()),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='processing_levels', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=2000)),
                ('thing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='core.thing')),
            ],
        ),
        migrations.CreateModel(
            name='ObservedProperty',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('definition', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('variable_type', models.CharField(blank=True, max_length=500, null=True)),
                ('variable_code', models.CharField(blank=True, max_length=500, null=True)),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Datastream',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('observation_type', models.CharField(blank=True, max_length=255, null=True)),
                ('result_type', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('sampled_medium', models.CharField(blank=True, max_length=255, null=True)),
                ('value_count', models.IntegerField(blank=True, null=True)),
                ('no_data_value', models.FloatField(blank=True, max_length=255, null=True)),
                ('intended_time_spacing', models.FloatField(blank=True, max_length=255, null=True)),
                ('aggregation_statistic', models.CharField(blank=True, max_length=255, null=True)),
                ('time_aggregation_interval', models.FloatField(blank=True, max_length=255, null=True)),
                ('phenomenon_start_time', models.DateTimeField(blank=True, null=True)),
                ('phenomenon_end_time', models.DateTimeField(blank=True, null=True)),
                ('result_begin_time', models.DateTimeField(blank=True, null=True)),
                ('result_end_time', models.DateTimeField(blank=True, null=True)),
                ('is_visible', models.BooleanField(default=True)),
                ('data_source_column', models.CharField(blank=True, max_length=255, null=True)),
                ('data_source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.datasource')),
                ('intended_time_spacing_units', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='intended_time_spacing', to='core.unit')),
                ('observed_property', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.observedproperty')),
                ('processing_level', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='processing_level', to='core.processinglevel')),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='datastreams', to='core.sensor')),
                ('thing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datastreams', to='core.thing')),
                ('time_aggregation_interval_units', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time_aggregation_interval', to='core.unit')),
                ('unit', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='unit', to='core.unit')),
            ],
        ),
        migrations.CreateModel(
            name='ThingAssociation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owns_thing', models.BooleanField(default=False)),
                ('follows_thing', models.BooleanField(default=False)),
                ('is_primary_owner', models.BooleanField(default=False)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thing_associations', to=settings.AUTH_USER_MODEL)),
                ('thing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='associates', to='core.thing')),
            ],
            options={
                'unique_together': {('thing', 'person')},
            },
        ),
    ]