# Generated by Django 2.1 on 2018-08-04 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_remove_riderprofile_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='riderprofile',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.Event'),
        ),
    ]
