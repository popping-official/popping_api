from rest_framework import serializers
from .models import Brands, Product
from user.models import User

from map.serializers import LocationDictSerializer, Base64ImageField


class BrandSimpleSerializers(serializers.ModelSerializer):
	isSaved = serializers.SerializerMethodField()

	class Meta:
		model = Brands
		fields = ('id', 'name', 'description', 'thumbnail', 'isSaved')

	def get_isSaved(self, obj):
		user: User = self.context.get('user')
		try:
			state = user.followed.filter(id=obj.id).exists()
		except:
			return False
		return state


class ProductSimpleSerializers(serializers.ModelSerializer):
	isSaved = serializers.SerializerMethodField()

	class Meta:
		model = Product
		fields = ('id', 'name', 'description', 'thumbnail', 'isSaved', 'price')

	def get_isSaved(self, obj):
		user: User = self.context.get('user')
		try:
			state = user.savedProduct.filter(id=obj.id).exists()
		except:
			return False
		return state


class PopupStoreSimpleSerializer(serializers.Serializer):
	id = serializers.CharField(max_length=200)
	title = serializers.CharField(max_length=200)
	location = LocationDictSerializer(required=False)
	isSaved = serializers.SerializerMethodField(required=False)
	image = Base64ImageField(required=False)

	def get_isSaved(self, obj):
		user: User = self.context.get('user')
		try:
			return str(obj.id) in user.savedPopup
		except:
			return False







