# Generated by Django 2.0 on 2018-10-15 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0046_auto_20181015_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectpagecomponent',
            name='technology_component',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.TechnologyComponent'),
        ),
    ]
