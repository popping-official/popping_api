# map/utils.py

from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from mongoengine.queryset.visitor import Q
from config.settings import MONGO_DB_NAME
from .models import OfflinePopup, Place
from .serializers import PlaceSerializer, OfflinePopupStoreSerializer, OfflinePopupStoreSimpleSerializer, MainPopupSerializer
from .mongodb import MongoDBClient
from bson import ObjectId
from datetime import datetime

# main page 팝업 리스트들
@api_view(['GET'])
@permission_classes([AllowAny])
def main_popup(request):
    now = datetime.utcnow()
    collection = MongoDBClient.get_collection(MONGO_DB_NAME,'OfflinePopup')

    popularity_pipeline = [
        {
            "$match": {
                "status": 1
            }
        },
        {
            "$addFields": {
                "calculated_value": {
                    "$add": [
                        {"$multiply": [{"$ifNull": ["$saveCount", 0]}, 3]},
                        {"$ifNull": ["$viewCount", 0]}
                    ]
                }
            }
        },
        {
            "$match": {
                "$expr": {
                    "$and": [
                        {"$ne": ["$calculated_value", 0]},
                        {"$ne": ["$calculated_value", None]}
                    ]
                }
            }
        },
        {
            "$sort": {
                "calculated_value": -1
            }
        },
        {
            "$limit": 9
        }
    ]

    date_pipeline = [
        {
            "$match": {
                "status": 1
            }
        },
        {
            "$addFields": {
                "date_difference": {
                    "$abs": {
                        "$subtract": [now, "$date.start"]
                    }
                }
            }
        },
        {
            "$sort": {
                "date_difference": 1
            }
        },
        {
            "$limit": 9
        }
    ]

    # 집계 실행
    popularity_query = list(collection.aggregate(popularity_pipeline))
    date_query = list(collection.aggregate(date_pipeline))
    
    popularity_serializer = MainPopupSerializer(popularity_query, many=True)
    date_serializer = MainPopupSerializer(date_query, many=True)
    
    response_data = {
        'sortPopularity':popularity_serializer.data,
        'sortDate':date_serializer.data
    }
    
    return Response(response_data, status=status.HTTP_200_OK)
    
# 팝업리스트 api
@api_view(['GET'])
@permission_classes([AllowAny])
def offline_popups(request):
    response_data = {}
    
    context = {"user": request.user}
    
    sort_option = request.GET.get('sorted')
    district = request.GET.get('district')
    search = request.GET.get('search')
    
    # 모든 PopupStore 문서를 조회
    popupStore_query = OfflinePopup.objects.filter(status=1)
    
    # 자치구 필터링    
    if district:
        # location.address 필드에서 district를 포함하는 문서만 필터링
        popupStore_query = popupStore_query.filter(
            location__address__icontains=district
        )

    if search:
        # title 필드에 search가 포함되거나, badge 배열에 search가 포함된 문서만 필터링
        popupStore_query = popupStore_query.filter(
            Q(title__icontains=search) | Q(tag__in=[search])
        )
    # 정렬
    match sort_option:
        case "distance":
            
            geo_x = float(request.GET.get('geoX'))
            geo_y = float(request.GET.get('geoY'))
            
            # # x,y를 중심으로 팝업리스트 거리순 정렬
            popupStore_query = popupStore_query.filter(
                location__geoData__near=[geo_x, geo_y]
            )
        # 이건 api 호출보단 front에서 정렬하는게 나을듯???
        case "popularity":
            popupStore_query = popupStore_query.order_by('-viewCount')[:10]
        
        case _:
            pass
    
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
    
    radius_in_meters = int(request.GET.get('meter'))
    
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
        
        case "distance":
            
            # # x,y를 중심으로 팝업리스트 거리순 정렬
            nearby_locations = list(collection.find(query))
                
        case "popularity":
            nearby_locations = list(collection.find(query).sort("viewCount", -1))
            
    context = {"user": request.user}
    serializer = OfflinePopupStoreSimpleSerializer(nearby_locations, many=True, context=context)
    response_data = {
        'popupStores':serializer.data
    }
    
    return Response(response_data, status=status.HTTP_200_OK)

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
    
    pipeline = [
        {
            "$geoNear": {
                "near": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "distanceField": "distance",  # 거리 계산 결과를 저장할 필드
                "maxDistance": radius_in_meters,
                "spherical": True
            }
        },
    ]
    
    nearby_locations = list(collection.aggregate(pipeline))
    serializer = PlaceSerializer(nearby_locations, many=True)
    response_data = {
        'place':serializer.data
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
    
    # option = request.GET.get('option')
    
    # match option:
        
    #     case "popup":
    #         data_query = OfflinePopup.objects.get(id=popupId)
    #     case "place":
    #         data_query = Place.objects.get(id=popupId)
    
    data_query = OfflinePopup.objects.get(id=popupId)            
    data_query.viewCount = data_query.viewCount + 1
    data_query.save()  # 변경된 내용을 저장
    
    return Response(status=status.HTTP_200_OK)


        


