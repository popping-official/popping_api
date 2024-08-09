from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework import status

from share.utills import error_response


@api_view(['POST'])
@permission_classes([AllowAny])
def user_brand_product_save_toggle(request) -> Response:
	from user.models import User
	from .models import Brands, Product

	user_info: User = request.user
	if user_info.is_anonymous:
		return error_response(code=1)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_offline_popup_save_toggle(request) -> Response:
	from user.models import User
	# from map.models import

	user_info: User = request.user
	if user_info.is_anonymous:
		return error_response(code=1)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_brand_follow_toggle(request) -> Response:
	from user.models import User
	from .models import Brands
	'''

	:return: Response
	'''

	bid = request.data.get('bid')

	if bid is None:
		return error_response(code=3, field_name='Brand ID')

	try:
		brand_info: Brands = Brands.objects.get(id=bid)
	except ObjectDoesNotExist as e:
		return error_response(code=2, field_name='Brands')

	user_info: User = request.user
	if user_info.is_anonymous:
		return error_response(code=1)

	is_following = user_info.followed.filter(id=brand_info.pk).exists()

	if is_following:
		user_info.followed.remove(brand_info)
		return Response(status=status.HTTP_202_ACCEPTED)
	else:
		user_info.followed.add(brand_info)
		return Response(status=status.HTTP_201_CREATED)