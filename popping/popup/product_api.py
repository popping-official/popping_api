from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


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
	print(brand_info, product)

	try:
		product_info: Product = Product.objects.get(
			pk=product)
	except:
		return Response(status=status.HTTP_400_BAD_REQUEST)


	if product_info.brandFK == brand_info:
		return Response(ProductSerializer(product_info, context=context).data, status=status.HTTP_200_OK)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)
