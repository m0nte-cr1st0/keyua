# Generated by Django 2.0 on 2018-02-24 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_customerlogocomponent'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('button_title', models.CharField(blank=True, max_length=50, null=True)),
                ('button_url', models.CharField(blank=True, max_length=255, null=True)),
                ('view_type', models.PositiveSmallIntegerField(choices=[(1, 'Big-Small'), (2, 'Default')], default=((1, 'Big-Small'), (2, 'Default')))),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
