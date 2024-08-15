from rest_framework import serializers
from .models import Brands, Product
from user.models import User


class BrandsSerializer(serializers.ModelSerializer):
    isSaved = serializers.SerializerMethodField()
    class Meta:
        model = Brands
        fields = '__all__'

    def get_isSaved(self, obj):
        user: User = self.context.get('user')
        try:
            state = user.followed.filter(id=obj.id).exists()
        except:
            return False
        return state

    def create(self, validated_data):
        return Brands.objects.create(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    isSaved = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        brand = validated_data.pop('brandFK')
        product = Product.objects.create(brandFK=brand, **validated_data)
        return product

    def get_isSaved(self, obj):
        user: User = self.context.get('user')
        try:
            state = user.savedProduct.filter(id=obj.id).exists()
        except:
            return False
        return state
