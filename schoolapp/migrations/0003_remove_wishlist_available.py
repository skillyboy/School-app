# Generated by Django 3.2.9 on 2022-05-25 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0002_auto_20220523_1354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='available',
        ),
    ]
