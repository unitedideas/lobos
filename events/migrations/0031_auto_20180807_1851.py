# Generated by Django 2.1 on 2018-08-08 01:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0030_remove_riderprofile_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='riderprofile',
            old_name='Registration_date_time',
            new_name='registration_date_time',
        ),
    ]
