# Generated by Django 2.0 on 2019-01-31 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0054_columnimagewithlistcomponent_columns_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='columnimagecomponent',
            name='columns_count',
            field=models.CharField(choices=[('col-md-6', 'Two columns'), ('col-sm-4 col-xs-12', 'Tree columns'), ('col-md-3 col-sm-6 col-xs-12', 'Four columns')], default='col-md-6 col-sm-6', max_length=50),
        ),
    ]
