# Generated by Django 2.1 on 2018-08-08 01:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0026_auto_20180807_1829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='riderprofile',
            name='rider_class',
        ),
    ]