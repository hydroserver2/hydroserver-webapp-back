# Generated by Django 4.1 on 2023-08-21 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_is_verified_customuser_unverified_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='link',
            field=models.URLField(blank=True, max_length=2000, null=True),
        ),
    ]