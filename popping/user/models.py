from django.db import models
from share.models import TimeModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin, TimeModel):
    email = models.EmailField(
        max_length=50,
        unique=True,
    )
    name = models.CharField(
        # 일반유저만 실명을 기입함, 팝업 담당자는 X
        max_length=10,
        null=True,
        blank=True
    )
    nickname = models.CharField(
        # 일반유저 = 닉네임
        # 팝업 담당자 = 브랜드 네임
        max_length=25,
        unique=True,
    )
    isMale = models.BooleanField(
        null=True,
        blank=True
    )
    idNumber = models.CharField(
        # 일반 유저 = 주민등록번호 (personalNumber)
        # 팝업 담당자 = 사업자등록번호 (businessNumber)
        max_length=14,
    )
    phoneNumber = models.CharField(
        max_length=13,
    )
    authCode = models.CharField(
        max_length=8
    )
    uuid = models.UUIDField(
		default=uuid.uuid4
	)
    isPopper = models.BooleanField(
        default=False
    )
    is_staff = models.BooleanField(
        # django에서 필요한 필드기 때문에 python 문법으로 필드명 설정
        default=False
    )
    is_active = models.BooleanField(
        # django에서 필요한 필드기 때문에 python 문법으로 필드명 설정
        default=True
    )
    USERNAME_FIELD = 'email'

