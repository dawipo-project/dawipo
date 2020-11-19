# Generated by Django 3.1.2 on 2020-11-11 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=30)),
                ('zipcode', models.CharField(max_length=10)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
