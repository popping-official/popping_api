# Generated by Django 5.0.7 on 2024-08-15 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_rename_saved_product_user_savedproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phoneNumber',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
