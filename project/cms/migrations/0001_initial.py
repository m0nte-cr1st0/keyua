# Generated by Django 2.0 on 2018-02-24 15:04

from django.db import migrations, models
import django.db.models.deletion
import project.cms.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BottomComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('button_title', models.CharField(blank=True, max_length=50, null=True)),
                ('button_url', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, project.cms.models.Component),
        ),
        migrations.CreateModel(
            name='CityComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('cities', models.ManyToManyField(to='content.City')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, project.cms.models.Component),
        ),
        migrations.CreateModel(
            name='ComponentUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('component', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FourColumnComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('button_title', models.CharField(blank=True, max_length=50, null=True)),
                ('button_url', models.CharField(blank=True, max_length=255, null=True)),
                ('background', models.ImageField(upload_to='backgrounds/')),
                ('columns', models.ManyToManyField(to='content.Column')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, project.cms.models.Component),
        ),
        migrations.CreateModel(
            name='HeaderComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('background', models.ImageField(upload_to='backgrounds/')),
                ('css_style', models.PositiveSmallIntegerField(choices=[(1, 'As on main page'), (2, 'With white menu links'), (3, 'With black menu links')])),
                ('sub_title', models.CharField(max_length=255)),
                ('top_button_title', models.CharField(blank=True, max_length=50, null=True)),
                ('top_button_url', models.CharField(blank=True, max_length=255, null=True)),
                ('white_button_title', models.CharField(blank=True, max_length=50, null=True)),
                ('white_button_url', models.CharField(blank=True, max_length=255, null=True)),
                ('green_button_title', models.CharField(blank=True, max_length=50, null=True)),
                ('green_button_url', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, project.cms.models.Component),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('js_code', models.TextField(blank=True, null=True)),
                ('meta_title', models.CharField(max_length=255)),
                ('meta_description', models.TextField()),
                ('meta_keywords', models.TextField(blank=True, null=True)),
                ('url', models.CharField(max_length=255, unique=True)),
                ('show_on_main_menu', models.BooleanField(default=False)),
                ('is_index', models.BooleanField(default=False)),
                ('is_draft', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PageComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.ComponentUnit')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Page')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='TechnologyComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('button_title', models.CharField(blank=True, max_length=50, null=True)),
                ('button_url', models.CharField(blank=True, max_length=255, null=True)),
                ('technologies', models.ManyToManyField(to='content.Technology')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, project.cms.models.Component),
        ),
        migrations.AddField(
            model_name='page',
            name='components',
            field=models.ManyToManyField(through='cms.PageComponent', to='cms.ComponentUnit'),
        ),
        migrations.AddField(
            model_name='page',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.Page'),
        ),
    ]
