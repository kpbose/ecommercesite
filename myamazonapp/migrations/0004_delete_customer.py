# Generated by Django 4.1.6 on 2023-06-09 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myamazonapp', '0003_alter_address_customer_alter_order_customer'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
