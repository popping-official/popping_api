from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponse
from rest_framework.views import APIView
import gridfs
from map.mongodb import MongoDBClient
import base64
from bson import ObjectId

class GridFSImageView(APIView):
    
    db = MongoDBClient.get_database('poppingmongo')
    fs = gridfs.GridFS(db)
    
    def get(self, request, *args, **kwargs):
        # 쿼리 파라미터에서 fileName 리스트 가져오기
        file_names = request.GET.getlist('fileName')
        
        if not file_names:
            return HttpResponse(status=400)  # 잘못된 요청
        
        images = []
        
        for file_id_str in file_names:
            try:
                # 문자열을 ObjectId로 변환
                file_id = ObjectId(file_id_str)
                
                # GridFS에서 파일 가져오기
                file = self.fs.get(file_id)
                encoded_img = base64.b64encode(file.read()).decode('utf-8')
                
                images.append(encoded_img)
            
            except Exception as e:
                # 예외 처리 (파일을 찾을 수 없는 경우)
                print(f"Error retrieving file with ID {file_id_str}: {e}")
        
        response = {
            'img': images
        }
        return Response(response, status=status.HTTP_200_OK)