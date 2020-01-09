# Generated by Django 2.0 on 2018-02-25 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('content', '0011_auto_20180225_0635'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Article')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('background', models.ImageField(help_text='Background or some image', upload_to='backgrounds/')),
                ('linkedin_url', models.CharField(blank=True, max_length=200, null=True)),
                ('properties', models.ManyToManyField(to='content.ListItem')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TextContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('css_style', models.CharField(blank=True, choices=[('h1', 'H1'), ('h2', 'H2'), ('text', 'Simple text'), ('numeric', 'Numeric list'), ('point', 'Point list'), ('marked-text', 'Left green border'), ('grey-text', 'Green text')], max_length=100, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='articles_images/')),
            ],
        ),
        migrations.AddField(
            model_name='articlecontent',
            name='content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.TextContent'),
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Author'),
        ),
        migrations.AddField(
            model_name='article',
            name='contents',
            field=models.ManyToManyField(through='blog.ArticleContent', to='blog.TextContent'),
        ),
        migrations.AddField(
            model_name='article',
            name='related_articles',
            field=models.ManyToManyField(related_name='_article_related_articles_+', to='blog.Article'),
        ),
    ]
