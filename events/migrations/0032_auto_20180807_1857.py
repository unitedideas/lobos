# Generated by Django 2.1 on 2018-08-08 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0031_auto_20180807_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='riderprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('Female', 'Female'), ('Male', 'Male')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='riderprofile',
            name='rider_class',
            field=models.CharField(blank=True, choices=[('Expert Schedule Classes - Over age 16', 'Expert Schedule Classes - Over age 16'), ('Expert Schedule Classes - 16 and under', 'Expert Schedule Classes - 16 and under'), ('Amateur Schedule Classes - Over age 16', 'Amateur Schedule Classes - Over age 16'), ('Expert Schedule Classes - 16 and under', 'Expert Schedule Classes - 16 and under'), ('Class 60 and 70 Rider', 'Class 60 and 70 Rider'), ('Escort Rider', 'Escort Rider')], max_length=100, null=True),
        ),
    ]
