# Generated by Django 5.1.1 on 2024-09-18 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_movie_rating_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]