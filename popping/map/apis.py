# map/utils.py

from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import PopupStore, Place, LocationDict
from .serializers import PopupStoreSerializer, PlaceSerializer
from .utills import crawling_data, json_test, insert_mongo, geocode_address
from .mongodb import MongoDBClient
from tqdm import tqdm
import json


@api_view(['GET'])
@permission_classes([AllowAny])
def store_list(request):
    # 기본적으로 모든 PopupStore 문서를 조회합니다
    popupStore_query = PopupStore.objects()
    
    # district 파라미터를 GET 요청에서 가져옵니다
    district = request.GET.get('district')
    
    if district:
        # location.address 필드에서 district를 포함하는 문서만 필터링합니다
        popupStore_query = popupStore_query.filter(
            location__address__icontains=district
        )
        
    # 시리얼라이저를 사용하여 데이터 직렬화
    serializer = PopupStoreSerializer(popupStore_query, many=True)
    
    # 응답 데이터 준비
    response_data = {
        'popupStores': serializer.data
    }
    
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def surround_place(request,option):
    response_data = {}
    popup_id = request.GET.get('popupId')
    radius_in_meters = int(request.GET.get('meter'))
    
    popup_store = PopupStore.objects.get(id=popup_id)
    
    latitude = popup_store.location.geoData['coordinates'][1]
    longitude = popup_store.location.geoData['coordinates'][0]
    
    collection = MongoDBClient.get_collection('poppingmongo','Place')
    
    query = {
        "option": option,
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
        'placeData':serializer.data
    }
                
    return Response(response_data, status=status.HTTP_200_OK)
        

@api_view(['GET'])
@permission_classes([AllowAny])
def daco_crawling(request):
    '''
        food inserted = '밥집', '술집', '고깃집', '한식', '일식', '횟집', 
            '양식', '중식', '국물요리', '해산물', '면요리', 
            '이탈리안', '뷔페', '분식', '태국음식', '베트남음식', 
            '패스트푸드', '멕시칸'
            
        cafe inserted = '카페', '브런치', '프렌치', '아이스크림', '케이크', '빙수', '디저트카페', '베이커리', '빵집' 
    '''
    
    food_category = []
    cafe_category = []
    
    place_list = []
    
    # 맛집 데이터 크롤링
    for category in tqdm(food_category):
        try:    
            url = f"https://www.diningcode.com/list.dc?query=서울{category}"
            place_list += crawling_data(request,url, 'food')
        except:
            continue
    
    # 카페 데이터 크롤링
    for category in tqdm(cafe_category):
        
        try:    
            url = f"https://www.diningcode.com/list.dc?query=서울{category}"
            place_list += crawling_data(request,url, 'cafe')
        except:
            continue
        
    insert_mongo(request, place_list, 'Place', 'many')
    
    response_data = {'message':f'{len(place_list)}개의 데이터 저장 성공'}
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def geo_addr(request):
    response_data = {}
    # collection = MongoDBClient.get_collection('poppingmongo','Place')
    # collection.create_index([("geoData", "2dsphere")])  # 올바른 인덱스 재생성
    # 기존 인덱스 정보 확인
    # print(collection.index_information())
    
    pass_list = []
    
    # 팝업 스토어
    # store_list = PopupStore.objects(
    #     location__geoData__exists=False
    # )
    # for store in store_list:
        
    #     for item in store.location:
            
    #         place_addr = geocode_address(item.address)
    #         if place_addr:
    #             try:
    #                 item.geoData = [float(place_addr['lon']),float(place_addr['lat'])]
    #                 store.save()
    #                 print(f"위도: {place_addr['lat']}, 경도: {place_addr['lon']}")
    #             except Exception as e:
    #                 print(e)
    #                 pass_list.append(store.title)
    #                 pass
    #         else:
    #             pass_list.append(store.title)
    #             print("지오코딩에 실패했습니다.")
    
    
    # 맛집 및 카페 스토어
    # place_list = Place.objects(geoData__exists=False)
    # for place in tqdm(place_list):
    #     place_addr = geocode_address(place.loadAddr)
    #     if place_addr:
    #         try:
    #             place.geoData = [float(place_addr['lon']),float(place_addr['lat'])]
    #             print(f"위도: {place_addr['lat']}, 경도: {place_addr['lon']}")
    #             place.save()
    #         except Exception as e:
    #             print(e)
    #             pass_list.append(place.title)
    #     else:
    #         pass_list.append(place.title)
    #         print("지오코딩에 실패했습니다.")
            
    response_data = {
        'pass_list':pass_list,
        'message':'geocoding 완료'
    }            
    return Response(response_data, status=status.HTTP_200_OK)

