# Generated by Django 5.0.7 on 2024-08-14 14:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0015_alter_user_saved_popup"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="saved_popup",
            new_name="savedPopup",
        ),
    ]
