# Generated by Django 4.1.6 on 2023-07-11 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myamazonapp', '0013_reviews_query'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='queri',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='query',
            name='subject',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
