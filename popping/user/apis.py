from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import SignUpSerializer, UserSerializer, UserManagementSerializer
import requests, json
from pprint import pprint 
from share.utills import envbuild
from django.contrib.auth import authenticate, login, logout


@api_view(['POST'])
@permission_classes([AllowAny])
def signin_api(request):
    
    if request.user.is_authenticated:
        return Response({"detail": "이미 로그인이 되어있습니다."}, status=status.HTTP_400_BAD_REQUEST)

    email = request.data.get('email', '')
    password = request.data.get('password', '')
    user = authenticate(request, email=email, password=password)

    if user is not None:
        login(request, user)
        serializer = UserSerializer(user, method='get')
        response_body = {
            'user' : serializer.data
        }
        return Response(response_body, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def signout_api(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def duplicate_check_api(request, option):
    
    """_summary_
    
        닉네임, 이메일, 전화번호 중복검사 or 존재여부 체크 api
    """
    
    check_data = request.data.get('checkData', None)
    
    if not check_data:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    orm_dict = {
        'nickname' : User.objects.filter(nickname=check_data).exists(),
        'brandName' : User.objects.filter(nickname=check_data).exists(),
        'email' : User.objects.filter(email=check_data).exists(),
        'phone' : User.objects.filter(phoneNumber=check_data).exists(),
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
    from .utills import send_auth_email
    
    target_email = request.data.get('email', None)

    if not target_email:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    subject = '[POPPING] 회원가입 인증 번호 전송'
    purpose_message = '회원가입에 앞서 이메일 인증을 위해'
    target_email = [target_email]
    
    auth_code = send_auth_email(
        target_email=target_email,
        subject=subject,
        purpose_message=purpose_message
    )    

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
    """_summary_
        회원가입 API
    """
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.create(serializer.validated_data)
        serializer = UserSerializer(user, method='get')
        response_body = {
            'user' : serializer.data
        }
        return Response(response_body, status=status.HTTP_201_CREATED)
                 

class UserAPI(APIView):
    """_summary_
        유저 RUD
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        serializer = UserSerializer(user, method='get')
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        return Response(status=status.HTTP_200_OK)
    
    def delete(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)



class UserManagementAPI(APIView):
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, option):
        option_list = ['email', 'auth', 'password']
        
        if not option in option_list:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserManagementSerializer(data=request.data, option=option, method='post')
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if option == 'email':
            # 이메일 찾기
            response_data = {
                'isExist' : False,
                'email' : ''
            }
            email = serializer.find_email(validated_data=serializer.validated_data)
            if email:
                response_data['isExist'] = True
                response_data['email'] = email
        elif option == 'auth': 
            # 비밀번호 재설정을 위한 인증메일 전송
            is_send = serializer.password_auth(validated_data=serializer.validated_data)
            response_data = {
                'isSend' : is_send,
            }
        else:
            # 비밀번호 재설정 링크 전송
            is_send = serializer.send_password_reset_email(validated_data=serializer.validated_data)
            response_data = {
                'isSend' : is_send,
            }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    
    def patch(self, request, option):
        
        serializer = UserManagementSerializer(data=request.data, option=option, method='patch')
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        is_success = serializer.update_password(validated_data=serializer.validated_data)
        
        return Response({ 'isSuccess' : is_success }, status=status.HTTP_200_OK)
        