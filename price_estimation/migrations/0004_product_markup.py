# Generated by Django 4.2.4 on 2023-08-29 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price_estimation', '0003_alter_product_batches_per_month'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='markup',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
