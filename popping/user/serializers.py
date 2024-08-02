from rest_framework import serializers
from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField()
    nickname = serializers.CharField()
    name = serializers.CharField(required=False)
    isMale = serializers.BooleanField(required=False)
    businessNumber = serializers.CharField(required=False)
    phoneNumber = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'nickname', 'name', 'isMale', 'businessNumber', 'phoneNumber', 'password')
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
        
