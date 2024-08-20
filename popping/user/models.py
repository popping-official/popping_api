from django.db import models
from share.models import TimeModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    

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
        null=True,
        blank=True
    )
    profileImage = models.TextField(
        default='/images/dummy/dummy_profile.jpg'
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
    gradeFK = models.ForeignKey(
        # 등급
        'user.UserGrade',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    followed = models.ManyToManyField(
        'popup.Brands',
        related_name='followers'  # 역 참조를 위한 필드명 설정
        )

    savedProduct = models.ManyToManyField(
        'popup.Product',
        related_name='saving_product'
        )

    savedPopup = models.JSONField(
        default=list
    )

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
    def get_by_natural_key(self, email):
        return self.get(email=email)


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


class PointHistory(TimeModel):
    userFK = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE
    )
    currentPoint = models.IntegerField(
        # 변경 이후 포인트 즉, 현재 포인트
        default=0
    )
    increasePoint = models.IntegerField(
        # 증가 포인트
        null=True,
        blank=True
    )
    decreasePoint = models.IntegerField(
        # 감소 포인트
        null=True,
        blank=True
    )
    PointChangeFK = models.ForeignKey(
        'user.PointChange',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
 
"""
    하단에 위치한 모델들은 인덱스 모델입니다.
"""


class AuthType(models.Model):
    type = models.TextField()
    

class UserGrade(models.Model):
    grade = models.CharField(
        # 등급명
        max_length=10
    )
    minOrderAmount = models.IntegerField(
        # 최소 주문금액
        default=0
    )
    maxOrderAmount = models.IntegerField(
        # 최대 주문금액
        default=0
    )
    earnRate = models.FloatField(
        # 적립률
        default=0
    )
    discountRate = models.FloatField(
        # 할인률
        default=0
    )
    

class PointChange(models.Model):
    changeInfo = models.CharField(
        # 변경정보
        max_length=10
    )