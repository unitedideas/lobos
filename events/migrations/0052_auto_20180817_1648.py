# Generated by Django 2.1 on 2018-08-17 23:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0051_auto_20180817_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riderprofile',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
