# Generated by Django 5.0 on 2024-02-01 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_order_order_details_alter_order_payment_method_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
