# Generated by Django 3.1.2 on 2020-11-13 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_company_active'),
        ('orders', '0003_auto_20201111_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='company_orders', to='company.company'),
            preserve_default=False,
        ),
    ]