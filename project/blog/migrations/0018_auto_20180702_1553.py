# Generated by Django 2.0 on 2018-07-02 15:53

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_article_header_background'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='intro',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]
