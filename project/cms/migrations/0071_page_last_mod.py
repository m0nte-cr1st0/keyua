# Generated by Django 2.0 on 2019-08-21 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0070_auto_20190327_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='last_mod',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
