# Generated by Django 2.0 on 2018-11-18 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0048_auto_20181113_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tilecomponent',
            name='columns',
        ),
    ]
