# Generated by Django 3.2 on 2021-04-22 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quikstart', '0004_alter_tweets_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweets',
            name='photo',
            field=models.ImageField(upload_to=''),
        ),
    ]
