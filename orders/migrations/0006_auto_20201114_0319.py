# Generated by Django 3.1.2 on 2020-11-14 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_orderchanges'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderChanges',
            new_name='OrderChange',
        ),
    ]
