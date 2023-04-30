# Generated by Django 4.1.6 on 2023-02-16 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('extra', models.TextField(blank=True, null=True)),
                ('external_id', models.IntegerField(db_index=True, unique=True, verbose_name='External Id for Genre')),
                ('name', models.CharField(db_index=True, max_length=30, unique=True, verbose_name='Name of Genere')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('extra', models.TextField(blank=True, null=True)),
                ('external_id', models.IntegerField(db_index=True, unique=True, verbose_name='External Movie Id')),
                ('title', models.CharField(max_length=128, verbose_name='Name of Movie')),
                ('overview', models.TextField(blank=True, null=True, verbose_name='Description of Movie')),
                ('image', models.URLField(blank=True, null=True, verbose_name='Image URL field')),
                ('language', models.CharField(max_length=5, verbose_name='Movie Language')),
                ('popularity', models.FloatField(blank=True, null=True, verbose_name='Movie Popularity Score')),
                ('release_date', models.DateField(verbose_name='Movie Release Date')),
                ('revenue', models.FloatField(blank=True, null=True, verbose_name='Movie Total Revenue')),
                ('runtime', models.FloatField(verbose_name='Movie Runtime')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('genre', models.ManyToManyField(related_name='movie', to='home.genre')),
            ],
            options={
                'ordering': ('popularity',),
            },
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('extra', models.TextField(blank=True, null=True)),
                ('rating', models.FloatField(default=0.0, verbose_name='Rating for Movie')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('movies', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to='home.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlists', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
