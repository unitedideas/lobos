# Generated by Django 2.1 on 2018-08-08 01:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0029_auto_20180807_1846'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='riderprofile',
            name='gender',
        ),
    ]
