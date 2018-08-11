# Generated by Django 2.1 on 2018-08-11 02:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0038_remove_riderprofile_conf_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riderprofile',
            name='user',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
