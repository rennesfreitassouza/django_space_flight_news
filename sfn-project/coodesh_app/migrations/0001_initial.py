# Generated by Django 4.0.2 on 2022-02-24 09:07

import coodesh_app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SFNArticles',
            fields=[
                ('my_id', models.BigIntegerField(default=coodesh_app.models.Tmy_id.get_latest_my_id, primary_key=True, serialize=False)),
                ('api_id', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('imageUrl', models.CharField(max_length=255)),
                ('newsSite', models.CharField(max_length=255)),
                ('summary', models.TextField(blank=True)),
                ('updatedAt', models.DateTimeField()),
                ('publishedAt', models.DateTimeField()),
                ('featured', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='SFNArticlesLaunches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_launche_id', models.CharField(max_length=255)),
                ('provider', models.CharField(max_length=255)),
                ('sfnarticles', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coodesh_app.sfnarticles')),
            ],
        ),
        migrations.CreateModel(
            name='SFNArticlesEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_event_id', models.CharField(max_length=255)),
                ('provider', models.CharField(max_length=255)),
                ('sfnarticles', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coodesh_app.sfnarticles')),
            ],
        ),
    ]
