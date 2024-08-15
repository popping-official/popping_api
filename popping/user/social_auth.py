from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from share.utills import envbuild
import requests
from django.conf import settings
from django.contrib.auth import login
from .models import User, SocialUser, UserGrade
from .serializers import UserSerializer
# from django.shortcuts import redirect
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from django.http import Http404
# from .models import MUM_T_USER, MUM_T_SOCIAL_USER, MUM_T_TOKEN
# from .utills import envbuild, save_user_history
# import uuid

def get_random_nickname():
    import random
    import string
    characters = string.ascii_letters + string.digits 
    while True:
        random_name = ''.join(random.choice(characters) for _ in range(8))
        user_with_code = User.objects.filter(nickname=random_name).first()
        if not user_with_code:
            return random_name
        
# def get_jwt_token(user_instance):
#     from rest_framework_simplejwt.tokens import RefreshToken
#     refresh_token = RefreshToken.for_user(user_instance)
#     access_token = str(refresh_token.access_token)
#     return str(refresh_token), access_token


# @api_view(['GET'])
# def get_provider(request):
#     try:
#         provider = MUM_T_SOCIAL_USER.objects.filter(MUM_T_USER_ID=request.user.id).get().MUM_PROVIDER
#     except:
#         provider = ''
#     response_data = {'provider' : provider}
#     return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def social_login(request, provider):
        
    # 프론트에서 건네받은 인가코드
    response_data = {}
    code = request.data.get('code')
    env = envbuild()
    
    # 나중에settings 에서 가져오는걸로 수정
    request_url = request.build_absolute_uri()
    if 'localhost' in request_url:
        redirect_domain = 'http://localhost:3000'
    else:
        redirect_domain = 'https://popping.world.com'
        
    call_back_url = f"{redirect_domain}/member/social?provider={provider}"
    
    if provider == 'kakao':
        client_id = env.str("SOCIAL_AUTH_KAKAO_CLIENT_ID")
        ## 인가코드를 기반으로 카카오 api에게 access token을 발급 받음
        get_access_token_api = requests.post(
            "https://kauth.kakao.com/oauth/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "redirect_uri": call_back_url,
                "code": code
            },
        )
        
        # # access token 발급
        access_token = get_access_token_api.json().get("access_token")
        
        ### 발급 받은 access token을 기반으로 카카오 유저 정보 api를 호출
        user_data = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            },
        )

        # 응답받은 response에서 해당 유저의 카카오 계정 즉, 이메일을 추출    
        user_data = user_data.json()
        user_email = user_data['kakao_account']['email']
        
    elif provider == 'google':
        client_id = env.str("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
        client_secret = env.str("SOCIAL_AUTH_GOOGLE_SECRET")
        state = "K2qO4dZ4vM6b3fNcEx1g"
        
        get_access_token_api = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={call_back_url}&state={state}")
        
        access_token = get_access_token_api.json().get("access_token")
        
        user_data = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
        user_data = user_data.json()
        user_email = user_data['email']
        
    ## 공통로직  
    try:
        user_instance = User.objects.filter(email=user_email, isSocialUser=True).get()
        is_exist = SocialUser.objects.filter(userFK=user_instance.id, provider=provider).exists()
        if not is_exist:
            response_data['isSuccess'] = False
            response_data['message'] = '해당 이메일은 이미 타소셜 계정 혹은 일반 계정으로 회원가입이 되어있습니다.'
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST) 
    except:
        ### 새로 회원가입 할 때 중복된 이메일이 있는지 확인 필요
        is_registed = User.objects.filter(email=user_email).exists()
        if is_registed:
            response_data['isSuccess'] = False
            response_data['message'] = '해당 이메일은 이미 일반 회원가입이 되어있습니다.'
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        random_code = get_random_nickname()
        
        new_user = User.objects.create(
            email = user_email,
            nickname = random_code,
            name = random_code,
            isPopper = False,
            isSocialUser=True,
            gradeFK = UserGrade.objects.get(pk=2)
            
        )
        new_user.set_unusable_password()
        new_user.save()
        
        provider = SocialUser.objects.create(
            userFK = new_user,
            provider = provider,
        )
        provider.save()
        
        user_instance = new_user
        
    # 존재할 경우 로직
    login(request, user_instance)
    serializer = UserSerializer(user_instance, method='get')
    response_data['isSuccess'] = True
    response_data['user'] = serializer.data
        
    return Response(response_data, status=status.HTTP_200_OK)




# @api_view(['POST'])
# def social_resign(request, provider):
#     import json
#     code = request.data.get('code')
#     survey_data = json.loads(request.data['surveyData'])
    
#     env = envbuild()
#     redirect_domain = settings.REDIRECT_DOMAIN
#     call_back_url = f"{redirect_domain}/auth-social-access?provider={provider}"
    
#     if provider == 'kakao':
#         client_id = env.str("SOCIAL_AUTH_KAKAO_CLIENT_ID")
        
#         ## 인가코드를 기반으로 카카오 api에게 access token을 발급 받음
#         get_access_token_api = requests.post(
#             "https://kauth.kakao.com/oauth/token",
#             headers={"Content-Type": "application/x-www-form-urlencoded"},
#             data={
#                 "grant_type": "authorization_code",
#                 "client_id": client_id,
#                 "redirect_uri": call_back_url,
#                 "code": code
#             },
#         )
#         # access token 발급 성공
#         access_token = get_access_token_api.json().get("access_token")
        
#         unlink_response = requests.post(
#             "https://kapi.kakao.com/v1/user/unlink",
#             headers={
#                 "Authorization": f"Bearer {access_token}",
#             }
#         )
#         if not unlink_response.status_code == 200:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
            
#     save_user_history(user=request.user, survey=survey_data)
        
#     return Response(status=status.HTTP_200_OK)
