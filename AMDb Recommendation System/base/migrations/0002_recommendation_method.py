# Generated by Django 4.1.6 on 2023-02-21 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='method',
            field=models.CharField(default='content', max_length=32, verbose_name='Method of Recommendation Preparation'),
            preserve_default=False,
        ),
    ]