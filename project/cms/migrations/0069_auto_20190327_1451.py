# Generated by Django 2.0 on 2019-03-27 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0068_auto_20190327_0642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tilecomponent',
            name='column_count',
            field=models.CharField(choices=[('col-md-3 col-sm-6 col-xs-12', 'Four columns'), ('col-xs-4', 'Three columns'), ('col-md-6 col-sm-6 col-xs-12', 'Two columns')], default='col-xs-4', max_length=50),
        ),
    ]
