# Generated by Django 5.0.7 on 2024-08-17 12:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("popup", "0013_remove_cart_amount_cart_option"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="totalPrice",
        ),
    ]
