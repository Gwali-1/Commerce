# Generated by Django 4.0.5 on 2022-07-08 23:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_listing_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='created',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]