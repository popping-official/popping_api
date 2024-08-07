 
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import SignUpSerializer, UserSerializer
import requests, json
from pprint import pprint 
from share.utills import envbuild


@api_view(['POST'])
@permission_classes([AllowAny])
def duplicate_check_api(request, option):
    
    """_summary_
    
        닉네임, 브랜드명, 이메일 중복검사 or 존재여부 체크 api
    """
    
    check_data = request.data.get('checkData', None)
    
    if not check_data:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    orm_dict = {
        'nickname' : User.objects.filter(nickname=check_data).exists(),
        'brandName' : User.objects.filter(nickname=check_data).exists(),
        'email' : User.objects.filter(email=check_data).exists()
    }
    
    if not option or not option in orm_dict:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    response_data = { 'isExist' : orm_dict[option] }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_email_send_api(request):
    
    """_summary_
        인증 메일 전송 api 
        - Body에 담겨온 email 값으로 인증번호를 첨부하여 이메일을 전송
    """
    
    from share.utills import generate_auth_code
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    
    target_email = request.data.get('email', None)

    if not target_email:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    auth_code = generate_auth_code()

    # HTML 템플릿을 렌더링
    html_content = render_to_string('auth-mail.html', {'auth_code': auth_code})
    text_content = strip_tags(html_content)
    
    subject = '[POPPING] 이메일 인증 번호 전송'

    email = EmailMultiAlternatives(subject, text_content, 'app.popping@gmail.com', [target_email])
    # HTML 첨부
    email.attach_alternative(html_content, "text/html")
    email.send()

    response_data = {
        'authCode' : auth_code
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def check_business_registration_api(request):
    
    """_summary_
        사업자등록 여부 진위확인 api
        - body에 담겨온 데이터를 기반으로 국세청 api를 통해 사업자 진위여부를 판별
    """
    
    business_number = request.data.get('businessNumber', '0000000000')
    start_date = request.data.get('startDate', '20000101')
    participant_name = request.data.get('participantName', 'None')
    
    env = envbuild()
    service_key = env.str("OPEN_DATA_PORTAL_SECRET_KEY")
    
    headers = {
        'accept': 'application/json',
        'Authorization': service_key,
        'Content-Type': 'application/json',
    }

    params = {
        'serviceKey': service_key,
    }
    
    json_data = {
        "businesses": [
            {
            "b_no": business_number, # 사업자등록번호
            "start_dt": start_date, # 개업년월일
            "p_nm": participant_name, # 대표자명
            }
        ]
    }

    api_response = requests.post(
        'https://api.odcloud.kr/api/nts-businessman/v1/validate', 
        headers=headers, 
        params=params, 
        json=json_data
    )

    # '01' : 유효한 사업자 / '02' : 유효하지 않은 사업자
    valid_code = api_response.json()['data'][0]['valid']
    
    if valid_code == '01':
        is_valid = True
    elif valid_code == '02':
        is_valid = False

    return Response({ 'isValid' : is_valid }, status=status.HTTP_200_OK)



class SignUpAPI(APIView):
    def post(self, request):
        
        serializer = SignUpSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            

class UserAPI(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, uuid):
        user = User.objects.filter(uuid=uuid).first()
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        serializer = UserSerializer(user, method='get')
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, uuid):
        return Response(status=status.HTTP_200_OK)
    
    def delete(self, request, uuid):
        return Response(status=status.HTTP_204_NO_CONTENT)

