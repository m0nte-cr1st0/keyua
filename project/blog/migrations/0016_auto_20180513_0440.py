# Generated by Django 2.0 on 2018-05-13 04:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20180511_1147'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-date', '-id']},
        ),
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Publication date'),
        ),
    ]
