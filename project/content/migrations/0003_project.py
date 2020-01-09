# Generated by Django 2.0 on 2018-02-24 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_customerlogo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('description', models.TextField()),
                ('button_title', models.CharField(blank=True, max_length=50, null=True)),
                ('button_url', models.CharField(blank=True, max_length=255, null=True)),
                ('background', models.ImageField(upload_to='backgrounds/')),
                ('logo', models.ImageField(upload_to='project_logos/')),
                ('short_description', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
