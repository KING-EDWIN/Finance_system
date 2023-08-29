# Generated by Django 4.2.4 on 2023-08-29 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price_estimation', '0004_product_markup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='markup',
            field=models.DecimalField(decimal_places=2, default=20, max_digits=5),
        ),
    ]