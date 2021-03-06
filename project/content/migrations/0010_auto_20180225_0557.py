# Generated by Django 2.0 on 2018-02-25 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_auto_20180225_0522'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColumnImageWithList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('button_title', models.CharField(blank=True, max_length=50, null=True)),
                ('button_url', models.CharField(blank=True, max_length=255, null=True)),
                ('background', models.ImageField(help_text='Background or some image', upload_to='backgrounds/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='columnimagewithlist',
            name='items',
            field=models.ManyToManyField(to='content.ListItem'),
        ),
    ]
