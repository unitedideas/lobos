# Generated by Django 2.1 on 2018-08-08 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0027_remove_riderprofile_rider_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='riderprofile',
            name='rider_class',
            field=models.CharField(blank=True, choices=[('Expert Schedule Classes - Over age 16', 'Expert Schedule Classes - Over age 16'), ('Expert Schedule Classes - 16 and under', 'Expert Schedule Classes - 16 and under'), ('Amateur Schedule Classes - Over age 16', 'Amateur Schedule Classes - Over age 16'), ('Expert Schedule Classes - 16 and under', 'Expert Schedule Classes - 16 and under'), ('Class 60 and 70 Rider', 'Class 60 and 70 Rider'), ('Escort Rider', 'Escort Rider')], max_length=100, null=True),
        ),
    ]