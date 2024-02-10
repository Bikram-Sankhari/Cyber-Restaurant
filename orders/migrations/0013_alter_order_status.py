# Generated by Django 5.0 on 2024-02-06 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_order_transaction_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Initiated', 'Initiated'), ('Completed', 'Completed'), ('Pending', 'Pending'), ('Failed', 'Failed')], max_length=10),
        ),
    ]
