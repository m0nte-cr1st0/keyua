# Generated by Django 2.0 on 2019-08-28 14:17

from django.db import migrations, models
import project.mailing.models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0004_auto_20190327_0434'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactform',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=project.mailing.models.get_upload_path),
        ),
    ]
