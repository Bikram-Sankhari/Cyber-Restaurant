# Generated by Django 5.0 on 2024-01-15 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_alter_fooditem_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='image',
            field=models.ImageField(blank=True, default='food_images/unknown.jpg', upload_to='food_images/'),
        ),
    ]
