# Generated by Django 5.0.7 on 2024-08-09 07:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_usergrade_pointhistory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usergrade',
            old_name='goal',
            new_name='maxOrderAmount',
        ),
        migrations.AddField(
            model_name='user',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.usergrade'),
        ),
        migrations.AddField(
            model_name='usergrade',
            name='discountRate',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='usergrade',
            name='earnRate',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='usergrade',
            name='minOrderAmount',
            field=models.IntegerField(default=0),
        ),
    ]
