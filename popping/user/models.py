from django.db import models
from share.models import TimeModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin, TimeModel):
    
    '''
    1. 일반유저, 팝업 담당자 둘다 공통으로 사용하는 필드
    - email : 이메일
    - phoneNumber : 전화번호
    - nickname : 닉네임 / 브랜드네임
    - isPopper : True = 팝업 담당자 / False = 일반 유저

    2. 일반 유저만 사용하는 필드
    - name : 실명
    - isMale : 성별

    3. 팝업 담당자만 사용하는 필드
    - businessNumber : 사업자 등록증
    '''
    
    email = models.EmailField(
        max_length=50,
        unique=True,
    )
    nickname = models.CharField(
        # 일반유저한테는 닉네임
        # 팝업담당자한테는 브랜드네임
        max_length=25,
        null=True,
        blank=True,
    )
    name = models.CharField(
        # 일반유저만 기입
        max_length=12,
        null=True,
        blank=True
    )
    isMale = models.BooleanField(
        # 일반유저만 기입
        null=True,
        blank=True
    )
    businessNumber = models.CharField(
        # 팝업 담당자만 기입
        max_length=10,
        null=True,
        blank=True
    )
    phoneNumber = models.CharField(
        max_length=11,
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

