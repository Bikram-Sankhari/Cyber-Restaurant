# Generated by Django 5.0 on 2024-02-06 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='username',
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(max_length=50),
        ),
    ]
