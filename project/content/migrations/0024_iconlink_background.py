# Generated by Django 2.0 on 2019-03-11 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0023_auto_20190301_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='iconlink',
            name='background',
            field=models.ImageField(blank=True, null=True, upload_to='icons_set/'),
        ),
    ]
