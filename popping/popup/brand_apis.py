from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework import status

from share.utills import error_response


@api_view(['GET'])
@permission_classes([AllowAny])
def brand_data(request, name):
	from .models import Brands
	from user.models import User
	from .main_serializers import BrandsSerializer

	context = {"user": request.user}
	try:
		manager = User.objects.get(nickname=name, isPopper=True)
	except Exception as e:
		print(e)
		return Response(status=status.HTTP_400_BAD_REQUEST)

	try:
		brand_info: Brands = Brands.objects.get(manager=manager)
	except:
		return Response(status=status.HTTP_400_BAD_REQUEST)
	return Response(BrandsSerializer(brand_info, context=context).data ,status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def all_brand_data(request):
	from .models import Brands
	from .main_serializers import BrandSimpleSerializers

	context = {"user": request.user}

	try:
		brand_info: Brands = Brands.objects.all().order_by('-pk')
	except:
		return Response(status=status.HTTP_400_BAD_REQUEST)

	return Response(BrandSimpleSerializers(brand_info, context=context, many=True).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def online_popup_store_main_data(request, name):
	from .models import Brands, Product
	from user.models import User
	from .main_serializers import BrandsSerializer, ProductSerializer

	response_data = dict()

	context = {"user": request.user}

	try:
		manager = User.objects.get(nickname=name, isPopper=True)
	except:
		return Response(status=status.HTTP_400_BAD_REQUEST)

	try:
		brand_info: Brands = Brands.objects.get(manager=manager)
	except:
		return Response(status=status.HTTP_400_BAD_REQUEST)

	response_data['brand'] = BrandsSerializer(brand_info, context=context).data

	product_query = Product.objects.filter(brandFK=brand_info)
	response_data['product'] = ProductSerializer(product_query, context=context, many=True).data

	return Response(response_data,status=status.HTTP_200_OK)

