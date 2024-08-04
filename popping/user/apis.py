 
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import SignUpSerializer, UserSerializer

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


