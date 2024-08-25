# map/utils.py

from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from config.settings import MONGO_DB_NAME
from .models import OfflinePopup
from .serializers import PlaceSerializer, OfflinePopupStoreSerializer, OfflinePopupStoreSimpleSerializer
from .mongodb import MongoDBClient
from tqdm import tqdm
import json
from bson import ObjectId

# 팝업리스트 api
@api_view(['GET'])
@permission_classes([AllowAny])
def offline_popups(request):
    response_data = {}
    
    sort_option = request.GET.get('sorted')
    geo_x = float(request.GET.get('geoX'))
    geo_y = float(request.GET.get('geoY'))
    district = request.GET.get('district')
    
    # 모든 PopupStore 문서를 조회
    popupStore_query = OfflinePopup.objects.filter(status=1)
    
    # 자치구 필터링    
    if district:
        # location.address 필드에서 district를 포함하는 문서만 필터링합니다
        popupStore_query = popupStore_query.filter(
            location__address__icontains=district
        )

    # 정렬
    match sort_option:
        case "distance":
            # # x,y를 중심으로 팝업리스트 거리순 정렬
            popupStore_query = popupStore_query.filter(
                location__geoData__near=[geo_x, geo_y]
            )
        # 이건 api 호출보단 front에서 정렬하는게 나을듯???
        case "popularity":
            popupStore_query = popupStore_query.order_by('-viewCount')
    
    context = {"user": request.user}
    serializer = OfflinePopupStoreSimpleSerializer(popupStore_query, many=True, context=context)
    
    response_data = {
        'popupStores': serializer.data
    }
    
    return Response(response_data, status=status.HTTP_200_OK)

# 위치 중심 팝업 리스트 조회
@api_view(['GET'])
@permission_classes([AllowAny])
def surround_popup(request):
    response_data = {}
    
    radius_in_meters = 1000
    
    sort_option = request.GET.get('sorted')
    geo_x = float(request.GET.get('geoX'))
    geo_y = float(request.GET.get('geoY'))
    
    collection = MongoDBClient.get_collection(MONGO_DB_NAME,'OfflinePopup')
    
    query = {
        "location.geoData": {
            "$near": {
                "$geometry": {
                    "type": "Point", 
                    "coordinates": [geo_x, geo_y]
                },
                "$maxDistance": radius_in_meters
            }
        },
        "status":1
    }
    
    match sort_option:
            
        case "popularity":
            nearby_locations = list(collection.find(query).sort("viewCount", -1))
            
        case _:
            nearby_locations = list(collection.find(query))
    
    context = {"user": request.user}
    serializer = OfflinePopupStoreSimpleSerializer(nearby_locations, many=True, context=context)
    response_data = {
        'popupStores':serializer.data
    }
    
    return Response(response_data, status=status.HTTP_200_OK)

# 팝업 조회 api
@api_view(['GET'])
@permission_classes([AllowAny])
def popup_detail(request, popupId):
    response_data = {}
    
    context = {"user": request.user}
    
    popupStore_query = OfflinePopup.objects.get(id=popupId)
    serializer = OfflinePopupStoreSerializer(popupStore_query, context=context)
    response_data = {
        'popupData': serializer.data
    }
    return Response(response_data, status=status.HTTP_200_OK)

# 조회시 count api
@api_view(['GET'])
@permission_classes([AllowAny])
def count_view(request, popupId):
    
    popupStore_query = OfflinePopup.objects.get(id=popupId)
    popupStore_query.viewCount = popupStore_query.viewCount + 1
    popupStore_query.save()  # 변경된 내용을 저장
    
    return Response(status=status.HTTP_200_OK)

# 팝업 중심 place 조회 api
@api_view(['GET'])
@permission_classes([AllowAny])
def surround_place(request):
    response_data = {}
    popup_id = request.GET.get('popupId')
    radius_in_meters = int(request.GET.get('meter'))
    
    popup_store = OfflinePopup.objects.get(id=popup_id)
    
    latitude = popup_store.location.geoData['coordinates'][1]
    longitude = popup_store.location.geoData['coordinates'][0]
    
    collection = MongoDBClient.get_collection(MONGO_DB_NAME,'Place')
    
    query = {
        "geoData": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "$maxDistance": radius_in_meters
            }
        }
    }
    nearby_locations = list(collection.find(query))
    
    serializer = PlaceSerializer(nearby_locations, many=True)
    response_data = {
        'place':serializer.data
    }
                
    return Response(response_data, status=status.HTTP_200_OK)
        


