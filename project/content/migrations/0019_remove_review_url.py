# Generated by Django 2.0 on 2019-02-13 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0018_review_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='url',
        ),
    ]
