from django.db import models
from share.models import TimeModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid


# popup Brands
class Brands(models.Model):
    manager = models.ForeignKey(
        'user.User',
        on_delete=models.DO_NOTHING
        )

    name = models.TextField(
        # 브랜드의 이름
        max_length=200,
        unique=True,
        )

    logo = models.URLField(
        # 브랜드의 로고
        null=True,
        blank=True
        )

    description = models.TextField(
    )


    conditions = models.JSONField(
        # 브랜드 계약 조건
        # 수수료, 등등
        default=dict
        )

    proceeding = models.BooleanField(
        # 현재 온라인 팝업 진행 여부
        default=False
        )

    contractStart = models.DateTimeField(
        # 브랜드 계약 시작일
        null=True,
        blank=True
        )

    contractEnd = models.DateTimeField(
        # 브랜드 계약 만료일
        null=True,
        blank=True
        )

    saved = models.IntegerField(
        default=0
        )
    thumbnail = models.TextField(

        )



# online popup's products
class Product(TimeModel):
    brandFK = models.ForeignKey(
        'popup.Brands',
        on_delete=models.CASCADE
    )
    productInvoice = models.UUIDField(
        # 상품 uuid
        default=uuid.uuid4
    )
    description = models.TextField(
    )
    name = models.CharField(
        max_length=100,
    )
    price = models.IntegerField(
        # 상품 가격
    )
    option = models.JSONField(
        default=dict
    )
    saved = models.IntegerField(
        default=0
        )
    view = models.IntegerField(
        default=0
        )
    thumbnail = models.TextField(

        )


# order list
class Order(TimeModel):
    userFK = models.ForeignKey(
        'user.User',
        on_delete=models.DO_NOTHING
    )
    orderInvoice = models.UUIDField(
        # 오더 uuid
        default=uuid.uuid4
    )
    name = models.CharField(
        # 오더 이름
        max_length=30,
    )
    totalPrice = models.IntegerField(
        # 총 결제 가격
    )
    buyDate = models.DateTimeField(
        # 구매 날짜
        null=True,
        blank=True
    )
    currency = models.CharField(
        # 결제 통화
        max_length=5,
        default="KRW"
    )
    orderStatus = models.BooleanField(
        # 결제 완료 체크
        default=False
    )
    orderQuery = models.JSONField(
        # 결제 쿼리
        null=True,
        blank=True
    )
    paymentType = models.TextField(
        # 결제 타입
        null=True,
        blank=True
    )
    receiptURL = models.URLField(
        # 영수증 url
        null=True,
        blank=True
    )


# order customer service
class OrderCS(TimeModel):
    userFK = models.ForeignKey(
        'user.User',
        on_delete=models.DO_NOTHING
    )
    orderFK = models.ForeignKey(
        'popup.Order',
        on_delete=models.DO_NOTHING
    )
    productFK = models.ForeignKey(
        'popup.Product',
        on_delete=models.DO_NOTHING
    )
    option = models.JSONField(
        null=True,
        blank=True
    )
    
class Cart(TimeModel):
    userFK = models.ForeignKey(
        'user.User',
        on_delete=models.DO_NOTHING
    )
    productFK = models.ForeignKey(
        'popup.Product',
        on_delete=models.DO_NOTHING
    )
    totalPrice = models.IntegerField(
        # 총 결제 가격
    )
    


