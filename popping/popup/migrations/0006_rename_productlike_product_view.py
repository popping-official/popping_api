# Generated by Django 5.0.7 on 2024-08-14 18:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("popup", "0005_rename_follower_brands_saved"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="productLike",
            new_name="view",
        ),
    ]
