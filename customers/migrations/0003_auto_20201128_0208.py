# Generated by Django 3.1.2 on 2020-11-28 02:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_customer_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('contact',),
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='cust_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.customercontact'),
        ),
    ]
