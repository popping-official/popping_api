from rest_framework import serializers
from .models import Brands, Product


class BrandsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Brands
		fields = '__all__'

	def create(self, validated_data):
		return Brands.objects.create(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    brandFK = BrandsSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brands.objects.all(), source='brandFK', write_only=True
    )

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        brand = validated_data.pop('brandFK')
        product = Product.objects.create(brandFK=brand, **validated_data)
        return product