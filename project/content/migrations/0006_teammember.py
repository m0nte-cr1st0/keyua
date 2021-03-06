# Generated by Django 2.0 on 2018-02-24 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_column_css_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('description', models.TextField()),
                ('photo', models.ImageField(upload_to='team_photos/')),
                ('position', models.CharField(max_length=50)),
                ('linkedin_url', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
