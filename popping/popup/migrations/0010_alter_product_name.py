# Generated by Django 5.0.7 on 2024-08-15 16:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("popup", "0009_product_thumbnail"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]
