# Generated by Django 3.1.2 on 2020-11-28 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_company_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='currency',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
