# Generated by Django 3.1.2 on 2020-11-17 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_company_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, upload_to='company/logos'),
        ),
    ]
