# Generated by Django 3.2.9 on 2022-05-25 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0006_wishlist_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='description',
        ),
    ]
