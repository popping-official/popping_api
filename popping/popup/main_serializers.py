from rest_framework import serializers


from .models import Brands, Product, Cart, Order, OrderCS
from .sub_serializers import BrandSimpleSerializers, ProductSimpleSerializers, PopupStoreSimpleSerializer, OrderCSSerializers


from user.models import User


from map.serializers import PopupStoreSerializer
from map.models import PopupStore

class UserSavedListSerializer(serializers.ModelSerializer):
    brands = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    popups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('brands', 'products', 'popups')

    def get_brands(self, obj: User):
        return BrandSimpleSerializers(obj.followed.all(), many=True, context={'user': obj}).data

    def get_products(self, obj: User):
        return ProductSimpleSerializers(obj.savedProduct.all(), many=True, context={'user': obj}).data

    def get_popups(self, obj: User):
        queryset = PopupStore.objects.filter(pk__in=obj.savedPopup)
        return PopupStoreSimpleSerializer(queryset, many=True, context={'user': obj}).data


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


class CartSerializers(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ('id', 'product', 'option')

    def get_product(self, obj):
        return ProductSimpleSerializers(obj.productFK, context={'user': self.context.get('user')}).data


class PaymentDataSerializers(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ('id', 'totalPrice', 'totalDiscount', 'item', )

    def get_item(self, obj):
        queryset = OrderCS.objects.filter(orderFK=obj)
        return OrderCSSerializers(queryset, many=True).data







