# Generated by Django 5.0.7 on 2024-08-15 16:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("popup", "0008_brands_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="thumbnail",
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
