# Generated by Django 4.2.4 on 2023-08-28 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price_estimation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='batches_per_month',
            field=models.PositiveIntegerField(default=4),
        ),
    ]
