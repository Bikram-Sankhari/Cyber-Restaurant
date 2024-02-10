# Generated by Django 5.0 on 2024-01-31 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.CharField(primary_key=True, serialize=False)),
                ('delivery_first_name', models.CharField(max_length=50)),
                ('delivery_last_name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=80)),
                ('delivery_email', models.EmailField(max_length=120)),
                ('delivery_phone_number', models.CharField(max_length=12)),
                ('delivery_address', models.CharField(max_length=500)),
                ('delivery_country', models.CharField(max_length=15)),
                ('delivery_state', models.CharField(max_length=15)),
                ('delivery_city', models.CharField(max_length=15)),
                ('delivery_pin_code', models.CharField(max_length=6)),
                ('order_details', models.JSONField()),
                ('price_details', models.JSONField()),
                ('payment_method', models.CharField(choices=[('Paypal', 'Paypal'), ('Razorpay', 'Razorpay')], max_length=8)),
                ('transaction_id', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled')], default='Pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]