# Generated by Django 4.1.5 on 2023-02-22 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_membership_organization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='organizations',
        ),
        migrations.DeleteModel(
            name='Membership',
        ),
    ]
