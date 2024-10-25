from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from share.utills import error_response


@api_view(['POST'])
@permission_classes([AllowAny])
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
	from map.models import OfflinePopup

	if request.user.is_anonymous:
		return Response(status=status.HTTP_401_UNAUTHORIZED)

	user_info: User = request.user
	if user_info.is_anonymous:
		return error_response(code=1)

	toggle_mapping = {
		'Brands': (user_info.followed, Brands),
		'Product': (user_info.savedProduct, Product),
		'Popup': (user_info.savedPopup, OfflinePopup)
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
		return error_response(code=2, model_name=toggle_type)

	if toggle_type == 'Popup':
		if id in toggle:
			toggle.remove(id)
			info.saveCount -= 1
			toggle_status = False
		else:
			toggle.append(id)
			info.saveCount += 1
			toggle_status = True
	else:
		if toggle.filter(id=info.pk).exists():
			toggle.remove(info)
			info.saveCount -= 1
			toggle_status = False
		else:
			toggle.add(info)
			info.saveCount += 1
			toggle_status = True

	user_info.save()
	info.save()

	if toggle_status:
		return Response(status=status.HTTP_201_CREATED)
	else:
		return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@permission_classes([AllowAny])
def test_function_mongodb(request) -> Response:
	from map.models import OfflinePopup
	from map.serializers import OfflinePopupStoreSerializer
	if request.user.is_anonymous:
		return Response(status=status.HTTP_401_UNAUTHORIZED)

	context = {"user": request.user}

	popupStore_query = OfflinePopup.objects()

	serializer = OfflinePopupStoreSerializer(popupStore_query, many=True, context=context)

	response_data = {
		'popupStores': serializer.data
		}

	return Response(response_data, status=status.HTTP_200_OK)


# 총 3개의 데이터들을 한번에 가지고와서 뿌려주기.
# Product, Brands, PopupMap
@api_view(['GET'])
@permission_classes([AllowAny])
def user_follow_list_get(request) -> Response:
	from user.models import User
	from .main_serializers import UserSavedListSerializer
	if request.user.is_anonymous:
		return Response(status=status.HTTP_401_UNAUTHORIZED)

	userInfo: User = User.objects.get(pk=request.user.pk)

	return Response(UserSavedListSerializer(userInfo).data, status=status.HTTP_200_OK)


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def follow_count_get(request) -> Response:
# 	from user.models import User
# 	from .models import Brands
#
# 	if request.user.is_anonymous:
# 		return Response(status=status.HTTP_401_UNAUTHORIZED)
#
# 	user: User = request.user
#
# 	if user.isPopper:



