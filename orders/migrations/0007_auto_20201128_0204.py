# Generated by Django 3.1.2 on 2020-11-28 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20201114_0319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pre-order', 'Pre-order'), ('confirmed', 'Confirmed'), ('awaiting-advance-payment', 'Awaiting advance payment'), ('in-production', 'In Production'), ('scheduled', 'Scheduled for dispatch'), ('dispatched', 'Dispatched'), ('delivered', 'Delivered'), ('canceled', 'Canceled')], default='pre-order', max_length=25),
        ),
    ]
