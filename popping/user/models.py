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
    businessInfo = models.JSONField(
        # 팝업 담당자만 기입
        null=True,
        blank=True
    )
    phoneNumber = models.CharField(
        max_length=11,
    )
    authCode = models.CharField(
        # 인증번호용 컬럼
        max_length=8
    )
    authType = models.ForeignKey(
        # 인증 종류 => 어떤 이유로 인증코드를 발급받았는지
        'user.AuthType',
        on_delete=models.CASCADE,
        null=True,
        blank=True
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
    isSocialUser = models.BooleanField(
        # 소셜 로그인 유저 여부
        default=False
    )
    USERNAME_FIELD = 'email'


class SocialUser(TimeModel): 
    PROVIDER_CHOICES = [
        ('naver', 'naver'),
        ('kakao', 'kakao'),
        ('google', 'google'),
    ]
    userFK = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE
    )
    provider = models.CharField(
        max_length=10,
        choices=PROVIDER_CHOICES
    )

    
class AuthType(models.Model):
    type = models.TextField()
    

