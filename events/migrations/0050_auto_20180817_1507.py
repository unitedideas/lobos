# Generated by Django 2.1 on 2018-08-17 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0049_auto_20180817_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='escort_rider_cost',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='post_entry_cost',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='pre_entry_cost',
            field=models.IntegerField(),
        ),
    ]
