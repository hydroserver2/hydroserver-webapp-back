# Generated by Django 4.2.3 on 2023-08-15 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_orcid'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='unverified_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
