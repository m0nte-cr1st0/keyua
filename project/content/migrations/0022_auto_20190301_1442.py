# Generated by Django 2.0 on 2019-03-01 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0021_review_background_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iconlink',
            name='icon',
        ),
        migrations.AddField(
            model_name='iconlink',
            name='background',
            field=models.ImageField(blank=True, null=True, upload_to='icons_set/'),
        ),
    ]
