from rest_framework import serializers
from datetime import datetime

from .models import Brands, Product, OrderCS
from user.models import User
from map.serializers import LocationDictSerializer, Base64ImageField


class BrandSimpleSerializers(serializers.ModelSerializer):
	isSaved = serializers.SerializerMethodField()
	contractEnd = serializers.DateTimeField(format='%Y년 %m월 %d일')
	contractStart = serializers.DateTimeField(format='%Y년 %m월 %d일')
	proceeding = serializers.SerializerMethodField()
	isAble = serializers.SerializerMethodField()
	name = serializers.SerializerMethodField()

	class Meta:
		model = Brands
		fields = ('id', 'name', 'description', 'thumbnail', 'isSaved', 'proceeding', 'contractStart', 'contractEnd', 'saved', 'isAble')

	def get_isSaved(self, obj):
		try:
			user: User = self.context.get('user')
			state = user.followed.filter(id=obj.id).exists()
		except:
			return False
		return state

	def get_proceeding(self, obj):
		today = datetime.today().date()
		contract_start = obj.contractStart.date()  # DateTimeField를 Date로 변환
		contract_end = obj.contractEnd.date()  # DateTimeField를 Date로 변환

		if contract_start <= today <= contract_end:
			return 1
		elif today > contract_end:
			return 2
		else:
			return 0

	def get_isAble(self, obj):
		if self.get_proceeding(obj) == 1:
			return True
		else:
			return False

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





