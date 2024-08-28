from rest_framework import serializers
from datetime import datetime

from .models import Brands, Product, OrderCS
from user.models import User
from map.serializers import LocationDictSerializer, Base64ImageField


class BrandSimpleSerializers(serializers.ModelSerializer):
	isSaved = serializers.SerializerMethodField()
	contractEnd = serializers.DateTimeField()
	contractStart = serializers.DateTimeField()
	name = serializers.SerializerMethodField()

	class Meta:
		model = Brands
		fields = ('id', 'name', 'description', 'thumbnail', 'isSaved', 'contractStart', 'contractEnd', 'saved')

	def get_isSaved(self, obj):
		try:
			user: User = self.context.get('user')
			state = user.followed.filter(id=obj.id).exists()
		except:
			return False
		return state

	def get_name(self, obj: Brands):
		return obj.manager.nickname
  

class ProductSimpleSerializers(serializers.ModelSerializer):
    isSaved = serializers.SerializerMethodField()
    brandFK = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'thumbnail', 'isSaved', 'price', 'option', 'brandFK', 'saved')

    def get_isSaved(self, obj):
        try:
            user: User = self.context.get('user')
            state = user.savedProduct.filter(id=obj.id).exists()
        except:
            return False
        return state

    def get_brandFK(self, obj):
        return BrandSimpleSerializers(obj.brandFK).data

class PopupStoreSimpleSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200)
    title = serializers.CharField(max_length=200)
    location = LocationDictSerializer(required=False)
    isSaved = serializers.SerializerMethodField(required=False)
    image = Base64ImageField(required=False)

    def get_isSaved(self, obj):
        try:
            user: User = self.context.get('user')
            return str(obj.id) in user.savedPopup
        except:
            return False


class OrderCSSerializers(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    class Meta:
        model = OrderCS
        fields = ('id', 'product', 'option')

    def get_product(self, obj):
        return ProductSimpleSerializers(obj.productFK).data


class BrandManageSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        self.method = kwargs.pop('method', 'GET')
        super().__init__(*args, **kwargs)
        
        if self.method == 'GET':
            self.fields['id'] = serializers.IntegerField()
            self.fields['logo'] = serializers.CharField()
            self.fields['thumbnail'] = serializers.CharField()
            self.fields['description'] = serializers.CharField()
            
        elif self.method == 'POST' or self.method == 'PATCH':
            self.fields['logo'] = serializers.CharField()
            self.fields['thumbnail'] = serializers.CharField()
            self.fields['description'] = serializers.CharField()
        
            if self.method == 'PATCH':
                self.fields['brandId'] = serializers.IntegerField()
        
        
    class Meta:
        model = Brands
        fields = ()
    
    def create(self, validated_data):
        user = validated_data['user']
        del validated_data['user']
        brand = Brands(manager=user, **validated_data)
        brand.save()
        return brand
    
    def update(self, validated_data):
        brand_id = validated_data['brandId']
        del validated_data['brandId']
        brand_query = Brands.objects.filter(pk=brand_id)
        brand_query.update(**validated_data)