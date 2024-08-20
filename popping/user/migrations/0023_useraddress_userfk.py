# Generated by Django 5.0.7 on 2024-08-19 17:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0022_alter_useraddress_phonenumber_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="useraddress",
            name="userFK",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
