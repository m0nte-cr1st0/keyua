# Generated by Django 2.0 on 2018-11-18 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0016_customerlogo_url'),
        ('cms', '0049_remove_tilecomponent_columns'),
    ]

    operations = [
        migrations.CreateModel(
            name='TileColumnComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.Column')),
                ('tile_component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.TileComponent')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='tilecomponent',
            name='columns',
            field=models.ManyToManyField(through='cms.TileColumnComponent', to='content.Column'),
        ),
    ]
