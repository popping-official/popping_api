# Generated by Django 5.0.7 on 2024-08-13 13:58

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("popup", "0002_remove_brands_followers"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="buyDate",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="currency",
            field=models.CharField(default="KRW", max_length=5),
        ),
        migrations.AddField(
            model_name="order",
            name="name",
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="orderInvoice",
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name="order",
            name="orderQuery",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="orderStatus",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="order",
            name="paymentType",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="receiptURL",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="totalPrice",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="userFK",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ordercs",
            name="option",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="ordercs",
            name="orderFK",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="popup.order",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ordercs",
            name="productFK",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="popup.product",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ordercs",
            name="userFK",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="discription",
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="price",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="productInvoice",
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name="product",
            name="productLike",
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                ("updatedAt", models.DateTimeField(auto_now=True)),
                ("totalPrice", models.IntegerField()),
                (
                    "productFK",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="popup.product",
                    ),
                ),
                (
                    "userFK",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]
