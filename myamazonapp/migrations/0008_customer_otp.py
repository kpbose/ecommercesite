# Generated by Django 4.1.6 on 2023-06-12 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myamazonapp', '0007_customer_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='otp',
            field=models.IntegerField(default=100),
        ),
    ]
