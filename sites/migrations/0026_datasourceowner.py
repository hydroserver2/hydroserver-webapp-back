# Generated by Django 4.1 on 2023-07-10 20:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0025_dataloader_remove_datasource_owner_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSourceOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_primary_owner', models.BooleanField(default=False)),
                ('data_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.datasource')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('data_source', 'person')},
            },
        ),
    ]