# Generated by Django 5.0.7 on 2024-08-02 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_user_idnumber_user_businessnumber_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
