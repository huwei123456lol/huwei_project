# Generated by Django 3.1.2 on 2020-12-16 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('default_music', '0005_auto_20201215_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='author_birth',
            field=models.DateField(default='2020-12-16'),
        ),
        migrations.AlterField(
            model_name='author',
            name='author_dead_time',
            field=models.DateField(default='2020-12-16'),
        ),
    ]