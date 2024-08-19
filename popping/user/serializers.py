from rest_framework import serializers
from .models import User, SocialUser, UserGrade, AuthType, PointHistory
from .utills import change_point


class SignUpSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField()
    nickname = serializers.CharField()
    name = serializers.CharField(required=False)
    isMale = serializers.BooleanField(required=False, allow_null=True)
    businessInfo = serializers.JSONField(required=False)
    phoneNumber = serializers.CharField()
    password = serializers.CharField(write_only=True)
    isPopper = serializers.BooleanField()
    
    class Meta:
        model = User
        fields = ('email', 'nickname', 'name', 'isMale', 'businessInfo', 'phoneNumber', 'password', 'isPopper')
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        
        # 등급 체계
        pk_num = 1
        if not user.isPopper:
            pk_num = 2
            change_point(
                user_instance=user,
                is_increase=True,
                point=1500,
                type_num=1
            )
        user.gradeFK = UserGrade.objects.get(pk=pk_num)
        
        user.save()
        
        return user
        

class UserSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        self.method = kwargs.pop('method', 'get')
        super().__init__(*args, **kwargs)
        
        if self.method == 'get': 
            self.fields['nickname'] = serializers.CharField()
            self.fields['name'] = serializers.SerializerMethodField()
            self.fields['isMale'] = serializers.BooleanField()
            self.fields['businessInfo'] = serializers.SerializerMethodField()
            self.fields['phoneNumber'] = serializers.CharField()
            self.fields['uuid'] = serializers.CharField()
            self.fields['createdAt'] = serializers.DateTimeField(format='%Y.%m.%d')
            self.fields['isPopper'] = serializers.BooleanField()
            self.fields['isSocialUser'] = serializers.BooleanField()
            self.fields['socialLoginProvider'] = serializers.SerializerMethodField()
            self.fields['gradeInfo'] = serializers.SerializerMethodField()
            self.fields['point'] = serializers.SerializerMethodField()
        
        elif self.method == 'patch':
            self.fields['isPopper'] = serializers.BooleanField()
            self.fields['nickname'] = serializers.CharField()   
            self.fields['name'] = serializers.CharField(required=False) 
            self.fields['isMale'] = serializers.BooleanField(required=False, allow_null=True) 
    
    class Meta:
        model = User
        fields = ()
        depth = 1
        
    def get_name(self, obj):
        return obj.name or ''
    
    def get_businessInfo(self, obj):
        return obj.businessInfo or {}

    def get_socialLoginProvider(self, obj):
        if obj.isSocialUser:
            return SocialUser.objects.filter(userFK=obj).first().provider
        else:
            return ''
    
    def get_gradeInfo(self, obj):
        serializers = UserGradeSerializer(obj.gradeFK)
        return serializers.data

    def get_point(self, obj):
        point_history = PointHistory.objects.filter(userFK=obj).last()
        if not point_history:
            return 0
        # 포인트를 천 단위로 구분하여 포맷
        return "{:,}".format(point_history.currentPoint)
    

    def update_user(self, validated_data, user):
        is_popper = validated_data.get('isPopper')
        nickname = validated_data.get('nickname')
        
        user.nickname = nickname
        
        if not is_popper:
            name = validated_data.get('name')
            is_male = validated_data.get('isMale')
            user.name = name
            user.isMale = is_male
        user.save()
    
    
    
class UserGradeSerializer(serializers.ModelSerializer):
    
    earnRate = serializers.SerializerMethodField()
    discountRate = serializers.SerializerMethodField()
    
    class Meta:
        model = UserGrade
        fields = ('grade', 'minOrderAmount', 'maxOrderAmount', 'earnRate', 'discountRate')
        
    def convert_integer(self, float_num):
        return round(float_num * 100)
    
    def get_earnRate(self, obj):
        return self.convert_integer(obj.earnRate)
    
    def get_discountRate(self, obj):
        return self.convert_integer(obj.discountRate)  
    
    

class MyPageSerializer(serializers.ModelSerializer):
    
    followingNum = serializers.SerializerMethodField()
    point = serializers.SerializerMethodField()
    gradeInfo = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('followingNum', 'point', 'gradeInfo')
        depth = 1
        
    def get_point(self, obj):
        point_history = PointHistory.objects.filter(userFK=obj).last()
        if not point_history:
            return 0
        # 포인트를 천 단위로 구분하여 포맷
        return "{:,}".format(point_history.currentPoint)
    
    def get_gradeInfo(self, obj):
        serializers = UserGradeSerializer(obj.gradeFK)
        return serializers.data
    
    def get_followingNum(self, obj):
        # obj = user 
        return len(obj.followed.all())
    
    
class UserManagementSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        self.option = kwargs.pop('option', 'email')
        self.method = kwargs.pop('method', 'post')
        super().__init__(*args, **kwargs)
        
        if self.method == 'post':
            if self.option == 'email':
                # 이메일 찾기
                self.fields['name'] = serializers.CharField(required=False)
                self.fields['businessNumber'] = serializers.CharField(required=False)
                self.fields['phoneNumber'] = serializers.CharField()
                self.fields['isPopper'] = serializers.BooleanField()
                
            elif self.option == 'auth':
                # 비밀번호 인증메일 전송
                self.fields['email'] = serializers.EmailField()
                self.fields['phoneNumber'] = serializers.CharField()
                
            elif self.option == 'password':
                # 비밀번호 찾기
                self.fields['email'] = serializers.EmailField()
                self.fields['phoneNumber'] = serializers.CharField()
                self.fields['authCode'] = serializers.CharField()
        else:
            self.fields['newPassword'] = serializers.CharField()
            self.fields['uuid'] = serializers.CharField(allow_null=True)

    class Meta:
        model = User
        fields = ()
        
    
    def find_email(self, validated_data):
        is_popper = validated_data.get('isPopper')
        phone_number = validated_data.get('phoneNumber')
        
        if is_popper:
            business_number = validated_data.get('businessNumber')
            user = User.objects.filter(businessInfo__businessNumber=business_number, phoneNumber=phone_number).first()
        else: 
            name = validated_data.get('name')
            user = User.objects.filter(name=name, phoneNumber=phone_number).first()
            
        if not user:
            return None
        
        # 이메일 마스킹 작업
        email = user.email
        local_part, domain = email.split('@')
        
        if len(local_part) > 2:
            # @ 바로 앞 두 글자를 *로 대체
            masked_local_part = local_part[:-2] + '**'
        else:
            # 만약 로컬 파트가 2글자 이하라면 전체를 *로 대체
            masked_local_part = '*' * len(local_part)
        
        masked_email = masked_local_part + '@' + domain
        return masked_email
    
    
    def password_auth(self, validated_data):
        
        """
            비밀번호 재설정을 위한 인증메일 전송
        """
        
        email = validated_data.get('email')
        phone_number = validated_data.get('phoneNumber')

        user = User.objects.filter(email=email, phoneNumber=phone_number).first()
            
        if not user:
            return False
        
        
        from .utills import send_auth_email

        subject = '[POPPING] 인증 번호 전송'
        purpose_message = '본인 인증을 위해'
        target_email = [email]
        
        auth_code = send_auth_email(
            target_email=target_email,
            subject=subject,
            purpose_message=purpose_message
        )
        
        user.authCode = auth_code
        user.authType = AuthType.objects.get(pk=3)
        user.save()
        
        return True
        
        
    def send_password_reset_email(self, validated_data):
        
        """
            비밀번호 재설정 링크를 전송
        """
        
        email = validated_data.get('email')
        auth_code = validated_data.get('authCode')
        redirect_domain = validated_data.get('redirect_domain')
        
        user = User.objects.filter(email=email, authCode=auth_code).first()
        
        if not user:
            return False
        
        from .utills import send_link_email
        
        subject = '[POPPING] 비밀번호 재설정'
        purpose_message = '비밀번호 재설정'
        target_email = [email]
        
        is_send = send_link_email(
            target_email=target_email,
            subject=subject,
            purpose_message=purpose_message,
            link=f'{redirect_domain}/member/forgot-password/reset-password?uuid={user.uuid}'
        )
        
        return is_send
    
    
    def update_password(self, validated_data):
        uuid = validated_data.get('uuid')
        
        user = User.objects.filter(uuid=uuid).first()
        if not user:
            return False    
        
        newPassword = validated_data.get('newPassword')
        user.set_password(newPassword)
        user.save()
        
        return True