# Generated by Django 4.1.6 on 2023-06-09 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myamazonapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='address',
            name='zipcode',
            field=models.IntegerField(null=True),
        ),
    ]