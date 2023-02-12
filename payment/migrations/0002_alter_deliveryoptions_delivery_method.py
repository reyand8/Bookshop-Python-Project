# Generated by Django 4.1.5 on 2023-01-25 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryoptions',
            name='delivery_method',
            field=models.CharField(choices=[('IS', 'In Shop'), ('HD', 'Home Delivery'), ('DD', 'Digital Delivery')], help_text='Required', max_length=255, verbose_name='delivery_method'),
        ),
    ]
