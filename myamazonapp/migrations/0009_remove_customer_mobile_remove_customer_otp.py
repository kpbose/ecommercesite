# Generated by Django 4.1.6 on 2023-06-12 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myamazonapp', '0008_customer_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='otp',
        ),
    ]
