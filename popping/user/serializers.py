from rest_framework import serializers
from .models import User, SocialUser


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
        
        elif self.method == 'patch':
            pass        
    
    class Meta:
        model = User
        fields = ()
        
    def get_name(self, obj):
        return obj.name or ''
    
    def get_businessInfo(self, obj):
        return obj.businessInfo or {}

    def get_socialLoginProvider(self, obj):
        if obj.isSocialUser:
            return SocialUser.objects.filter(userFK=obj).first().provider
        else:
            return ''
        