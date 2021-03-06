# Generated by Django 3.1.2 on 2020-11-29 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20201128_0312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='retail_price',
            new_name='price_1',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='whole_sale_price',
            new_name='price_2',
        ),
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.RemoveField(
            model_name='product',
            name='measures',
        ),
        migrations.AddField(
            model_name='product',
            name='observations',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='price_3',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(blank=True, db_index=True, max_length=20, null=True),
        ),
    ]
