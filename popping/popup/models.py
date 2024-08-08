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

# online popup's products
class Product(TimeModel):
	name = models.CharField(
		max_length=30,
		)

	option = models.JSONField(
		default=dict
		)



# order list
class Order(TimeModel):
	pass

# order customer service
class OrderCS(TimeModel):
	pass




