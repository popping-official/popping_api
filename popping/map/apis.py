# map/utils.py

from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Maps
from .serializers import MapsSerializer
from .mongodb import MongoDBClient
from .utills import crawling_data


@api_view(['GET'])
@permission_classes([AllowAny])
def list_maps(request):

    ### pymongo
    # # db = MongoDBClient.get_database('mydatabase')
    # collection = MongoDBClient.get_collection('mydatabase', 'mycollection')

    # # 컬렉션에 접근하여 작업 수행
    # document = {"name": "Alice", "age": 30}
    # collection.insert_one(document)
    
    
    ### mongoengine
    maps = Maps.objects.all()  # 모든 문서 조회
    serializer = MapsSerializer(maps, many=True)
    response_data = {
        'maps':serializer.data
    }
        
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def pd_test(request):
    response_data = {}
    
    food_category = [
        '밥집', '술집', '고깃집', '한식', '일식', '횟집', 
        '양식', '중식', '국물요리', '해산물', '면요리', 
        '이탈리안', '뷔페', '분식', '태국음식', '베트남음식', 
        '패스트푸드', '멕시칸'
    ]
    cafe_category = ['카페', '브런치', '프렌치', '아이스크림', '케이크', '빙수', '디저트카페', '베이커리', '빵집' ]
    
    url = "https://www.diningcode.com/list.dc?query=서울맛집"
    crawling_data(request,url)
        
    return Response(response_data, status=status.HTTP_200_OK)



# '''
    # food
    # {
    #     "NEW_ADDRESS":"신주소", "SUBWAY_INFO":"교통정보", "POST_SN":"고유번호", "CMMN_HMPG_URL":"웹사이트",
    #     "CMMN_TELNO":"전화번호", "POST_URL":"콘텐츠URL", "CMMN_HMPG_LANG":"홈페이지 언어", "ADDRESS":"주소", "FD_REPRSNT_MENU":"대표메뉴",
    #     "CMMN_USE_TIME":"운영시간", "POST_SJ":"상호명", "LANG_CODE_ID":"언어"
    # }
    # '''
    
    # '''
    # cafe
    # {
    #     "ISREAM":"보증액", "JTUPSOMAINEDF":"전통업소주된음식", "FCTYPDTJOBEPCNT":"공장생산직종업원수", 
    #     "SITEPOSTNO":"소재지우편번호", "MONAM":"월세액", "TOTEPNUM":"총인원", "UPTAENM":"업태구분명",
    #     "FCTYSILJOBEPCNT":"공장판매직종업원수", "LASTMODTS":"최종수정일자", "HOFFEPCNT":"본사종업원수",
    #     "CLGENDDT":"휴업종료일자", "UPDATEGBN":"데이터갱신구분", "RDNWHLADDR":"도로명주소", "DCBYMD":"폐업일자",
    #     "SITEWHLADDR":"지번주소", "Y":"좌표정보(Y)", "HOMEPAGE":"홈페이지", "DTLSTATEGBN":"상세영업상태코드", "TRDSTATEGBN":"영업상태코드",
    #     "X":"좌표정보(X)", "OPNSFTEAMCODE":"개방자치단체코드", "APVPERMYMD":"인허가일자", "JTUPSOASGNNO":"전통업소지정번호", 
    #     "FCTYOWKEPCNT":"공장사무직종업원수", "WMEIPCNT":"여성종사자수", "UPDATEDT":"데이터갱신일자", 
    #     "BPLCNM":"사업장명", "WTRSPLYFACILSENM":"급수시설구분명", "SNTUPTAENM":"위생업태명", "CLGSTDT":"휴업시작일자",
    #     "RDNPOSTNO":"도로명우편번호", "ROPNYMD":"재개업일자", "MGTNO":"관리번호", "FACILTOTSCP":"시설총규모", 
    #     "MULTUSNUPSOYN":"다중이용업소여부", "LVSENM":"등급구분명", "TRDSTATENM":"영업상태명", "SITEAREA":"소재지면적",
    #     "TRDPJUBNSENM":"영업장주변구분명", "SITETEL":"전화번호", "APVCANCELYMD":"인허가취소일자", "BDNGOWNSENM":"건물소유구분명",
    #     "DTLSTATENM":"상세영업상태명", "MANEIPCNT":"남성종사자수"},
    # '''
    
    # food_dataPath = 'C:/Users/wogml/OneDrive/바탕 화면/foodData.json'
    # cafe_dataPath = 'C:/Users/wogml/OneDrive/바탕 화면/cafeData.json'
    
    # update_food_datapath = 'C:/Users/wogml/OneDrive/바탕 화면/update_food_data.json'
    # update_cafe_datapath = 'C:/Users/wogml/OneDrive/바탕 화면/update_cafe_data.json'
    
    # df = pd.read_json(update_food_datapath, lines=True)
    
    # # 불필요한 컬럼 제거
    # # df = df.drop(columns=['cmmn_hmpg_lang','post_url','lang_code_id','cmmn_hmpg_url','post_sn'])
    
    # # 컬럼의 값이 빈값인 데이터 제거
    # # df = df[df['new_address'].str.strip() != '']
    
    # column_name = {
    #     'new_address':'roadNameAddr',
    #     'post_sj':'tradeName',
    #     'address':'numberAddr',
    #     'cmmn_telno':'telNumber',
    #     'fd_reprsnt_menu':'foodMenu',
    #     'subway_info':'subwayInfo',
    #     'cmmn_use_time':'time'
    # }
    # df.columns = ['roadNameAddr','tradeName','numberAddr','telNumber','foodMenu','subwayInfo','time']

    # df.to_json(update_food_datapath, orient='records', lines=True, force_ascii=False)