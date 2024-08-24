from rest_framework.views import APIView

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.core.exceptions import ObjectDoesNotExist


class OrderApi(APIView):
	def get(self, request):
		from .models import Order, Brands
		from user.models import User, PointHistory, UserAddress, UserGrade
		from .main_serializers import PaymentDataSerializers
		from user.serializers import UserAddressSerializers, UserGradeSerializer

		try:
			oid = request.GET['oid']
		except:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		try:
			order_instance = Order.objects.get(orderInvoice=oid)
		except:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		if request.user.is_anonymous:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		if request.user.pk != order_instance.userFK.pk:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		response_data = dict()

		user: User = request.user

		response_data['brand'] = Brands.objects.get(proceeding=1).manager.nickname.upper()

		point_history = PointHistory.objects.filter(userFK=user).last()
		response_data['point'] = point_history.currentPoint

		response_data['order'] = PaymentDataSerializers(order_instance).data

		response_data['address'] = UserAddressSerializers(UserAddress.objects.filter(userFK=user).order_by('-pk')[:5], many=True).data

		response_data['grade'] = UserGradeSerializer(UserGrade.objects.exclude(pk=1), many=True).data
		response_data['userGrade'] = UserGradeSerializer(user.gradeFK).data

		return Response(response_data, status=status.HTTP_200_OK)

	def post(self, request):
		"""
		장바구니 상품 or 단일 상품 Order Create
		"""
		from .models import Order, OrderCS, Cart
		from user.models import User

		if request.user.is_anonymous:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		user: User = request.user

		total_price = request.data.get('totalPrice')
		cart_list: list = request.data.get('order')

		order_instance = Order(
			userFK=user,
			totalPrice=total_price,
			)
		try:
			order_instance.save()
		except Exception as e:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		cs_list = list()
		for cart in cart_list:
			cart: Cart = Cart.objects.get(pk=cart)
			if cart.userFK.pk != user.pk:
				return Response(status=status.HTTP_400_BAD_REQUEST)

			order_cs_instance: OrderCS = OrderCS(
				userFK=user,
				productFK=cart.productFK,
				orderFK=order_instance,
				option=cart.option
				)
			cs_list.append(order_cs_instance)
		try:
			OrderCS.objects.bulk_create(cs_list)
		except Exception as e:
			order_instance.delete()
			return Response(status=status.HTTP_400_BAD_REQUEST)

		Cart.objects.filter(pk__in=cart_list).delete()

		return Response({'oid': order_instance.orderInvoice}, status=status.HTTP_201_CREATED)


