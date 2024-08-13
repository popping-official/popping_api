from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework import status

from share.utills import error_response


@api_view(['POST'])
@permission_classes([AllowAny])
@
def user_follow_save_toggle(request) -> Response:
	'''
	Front End 에서 필요한 데이터
	type: (Brands, Product) 중 1
	id: 타입에 맞는 해당 model의 id 값

	:param request:
	:return:
	'''

	from user.models import User
	from .models import Brands, Product

	user_info: User = request.user
	if user_info.is_anonymous:
		return error_response(code=1)

	toggle_mapping = {
		'Brands': (user_info.followed, Brands),
		'Product': (user_info.saved_product, Product)
		}

	toggle_type = request.data.get('type', 'Brands')

	toggle, model = toggle_mapping.get(toggle_type, (None, None))

	if toggle is None:
		return error_response(code=3, field_name='type')

	id = request.data.get('id')

	if id is None:
		return error_response(code=3, field_name=f'{toggle_type} ID')

	try:
		info: model = model.objects.get(id=id)
	except ObjectDoesNotExist:
		return error_response(code=2, field_name=toggle_type)

	if toggle.filter(id=info.pk).exists():
		toggle.remove(info)
		return Response(status=status.HTTP_202_ACCEPTED)
	else:
		toggle.add(info)
		return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_follow_list_get(request) -> Response:


	return Response(status=status.HTTP_200_OK)