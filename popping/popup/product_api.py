from rest_framework.views import APIView

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.core.exceptions import ObjectDoesNotExist


@api_view(['GET'])
@permission_classes([AllowAny])
def product_data(request, brand, product):
	from .models import Brands, Product
	from .main_serializers import ProductSerializer
	context = {"user": request.user}

	try:
		brand_info: Brands = Brands.objects.get(name=brand)
	except:
		return Response(status=status.HTTP_400_BAD_REQUEST)

	try:
		product_info: Product = Product.objects.get(
			pk=product)
	except:
		return Response(status=status.HTTP_400_BAD_REQUEST)

	if product_info.brandFK == brand_info:
		return Response(ProductSerializer(product_info, context=context).data, status=status.HTTP_200_OK)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)


# Login Req
class CartAPI(APIView):
	def get(self, request):
		from .models import Brands, Cart
		from .main_serializers import CartSerializers

		if request.user.is_anonymous:
			return Response(status.HTTP_401_UNAUTHORIZED)

		response_data = dict()
		response_data['brand'] = Brands.objects.get(proceeding=1).name.upper()

		cart_query: Cart = Cart.objects.filter(userFK=request.user)
		response_data['cart'] = CartSerializers(cart_query, many=True).data

		return Response(response_data, status=status.HTTP_200_OK)

	def post(self, request):
		from user.models import User
		from .models import Cart, Product
		"""
			id: int -> product id
			amount: int -> product amount
			option: dict -> key: (Color, Size) value: (str, str)
		"""
		if request.user.is_anonymous:
			return Response(status.HTTP_401_UNAUTHORIZED)

		try:
			pid: int = request.data.get('id')
			amount: int = request.data.get('amount')
			option: dict = request.data.get('option')
		except:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		cart_list = [item[0] for item in Cart.objects.filter(userFK=request.user).values_list('productFK')]

		if pid in cart_list:
			return Response({'status': 1, 'message': '장바구니에 이미 존재하는 상품입니다.'},status=status.HTTP_400_BAD_REQUEST)
		option['amount'] = amount
		try:
			product_instance = Product.objects.get(pk=pid)
		except:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		Cart.objects.create(
			productFK=product_instance,
			option=option,
			userFK=request.user,
		)
		return Response(status=status.HTTP_201_CREATED)

	def patch(self, request):
		"""
		Updates the Cart instance based on the provided id and options.
		Expects:
		- id: number
		- option: { type: string, action: string }
		- original: { amount: int }
		"""
		from .models import Cart, Product

		if request.user.is_anonymous:
			return Response(status.HTTP_401_UNAUTHORIZED)

		cart_id = request.data.get('id')
		option = request.data.get('option')

		if not cart_id or not option :
			return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			cart_instance: Cart = Cart.objects.get(pk=cart_id)
		except ObjectDoesNotExist:
			return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

		product_instance: Product = cart_instance.productFK

		color_exists = any(original_option['name'] == option['color'] for original_option in product_instance.option[0]['option'])
		size_exists = any(original_option['name'] == option['size'] for original_option in product_instance.option[1]['option'])

		if color_exists and size_exists:
			cart_instance.option = option
			cart_instance.save()

		return Response({'amount': cart_instance.option['amount']}, status=status.HTTP_202_ACCEPTED)

	def delete(self, request):
		from .models import Cart

		if request.user.is_anonymous:
			return Response(status.HTTP_401_UNAUTHORIZED)

		cart_id = request.data.get('id')

		cart_instance = Cart.objects.get(pk=cart_id)
		cart_instance.delete()

		return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@permission_classes([AllowAny])
def cart_count_get(request):
	from .models import Cart

	if request.user.is_anonymous:
		return Response(status.HTTP_401_UNAUTHORIZED)

	cart_instance: list[Cart] = Cart.objects.filter(userFK=request.user)

	return Response({'count': len(cart_instance)}, status=status.HTTP_200_OK)
