# Generated by Django 5.0.7 on 2024-08-20 02:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0024_useraddress_default"),
    ]

    operations = [
        migrations.AddField(
            model_name="usergrade",
            name="color",
            field=models.CharField(default=0, max_length=7),
            preserve_default=False,
        ),
    ]
