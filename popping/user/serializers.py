from rest_framework import serializers
from .models import User, SocialUser, UserGrade, AuthType


class SignUpSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField()
    nickname = serializers.CharField()
    name = serializers.CharField(required=False)
    isMale = serializers.BooleanField(required=False)
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
        pk_num = 2
        if user.isPopper:
            pk_num = 1
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
            self.fields['point'] = serializers.IntegerField()
        
        elif self.method == 'patch':
            pass        
    
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
                self.fields['name'] = serializers.CharField(required=False)
                self.fields['businessNumber'] = serializers.CharField(required=False)
                self.fields['email'] = serializers.EmailField()
                self.fields['isPopper'] = serializers.BooleanField()
                
            elif self.option == 'password':
                # 비밀번호 찾기
                self.fields['name'] = serializers.CharField(required=False)
                self.fields['businessNumber'] = serializers.CharField(required=False)
                self.fields['email'] = serializers.EmailField()
                self.fields['isPopper'] = serializers.BooleanField()
                self.fields['authCode'] = serializers.CharField()
        else:
            # patch
            pass        

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
        
        is_popper = validated_data.get('isPopper')
        email = validated_data.get('email')
        
        if is_popper:
            business_number = validated_data.get('businessNumber')
            user = User.objects.filter(businessInfo__businessNumber=business_number, email=email).first()
        else: 
            name = validated_data.get('name')
            user = User.objects.filter(name=name, email=email).first()
            
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
        
        is_popper = validated_data.get('isPopper')
        email = validated_data.get('email')
        auth_code = validated_data.get('authCode')
        
        if is_popper:
            business_number = validated_data.get('businessNumber')
            user = User.objects.filter(businessInfo__businessNumber=business_number, email=email, authCode=auth_code, authType=3).first()
        else: 
            name = validated_data.get('name')
            user = User.objects.filter(name=name, email=email, authCode=auth_code, authType=3).first()
            
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
            link='https://popping.world/api/'
        )
        
        return is_send