from rest_framework import serializers
from user.models import User
import base64
from django.core.files.base import ContentFile
import gridfs
from map.mongodb import MongoDBClient
from django.core.cache import cache
from bson import ObjectId

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            # 이미지 데이터를 Base64로 인코딩하는 경우
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)

    def to_representation(self, value):
        # 데이터베이스에서 이미지 데이터를 읽어올 때 Base64로 인코딩
        if value:
            return base64.b64encode(value.read()).decode('utf-8')
        return None

class LocationDictSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=200)
    placeName = serializers.CharField(max_length=100)
    geoData = serializers.JSONField(required=False)

class DateDictSerializer(serializers.Serializer):
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)
    
class PlaceSerializer(serializers.Serializer):
    # id = serializers.CharField(max_length=200)
    # id = serializers.CharField(source='_id', read_only=True)
    title = serializers.CharField(max_length=200)
    bestMenu = serializers.ListField(child=serializers.CharField(), required=False)
    # gradePoint = serializers.IntegerField()
    loadAddr = serializers.CharField(max_length=200)
    # numberAddr = serializers.CharField(max_length=200)
    # telNumber = serializers.CharField(max_length=200)
    option = serializers.CharField(max_length=200)
    # charTag = serializers.ListField(child=serializers.CharField(), required=False)
    # tags = serializers.ListField(child=serializers.CharField(), required=False)
    geoData = serializers.JSONField(required=False)
    image = serializers.SerializerMethodField(required=False)
    distance = serializers.IntegerField(required=False)
    
    def get_image(self, obj):
        
        db = MongoDBClient.get_database('poppingmongo')
        fs = gridfs.GridFS(db)
        
        try:
            img_id = str(obj.img.grid_id)
        except:
            img_id = str(obj.get('img'))
            
        cache_key = f"popup_image_{img_id}"
        encoded_img = cache.get(cache_key)
        
        if not encoded_img:
            file = fs.get(ObjectId(img_id))
            
            encoded_img = base64.b64encode(file.read()).decode('utf-8')
            cache.set(cache_key, encoded_img, timeout=60*60*24)  # 24시간 동안 캐시
            
        return encoded_img
    
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     ret['id'] = str(ret['id'])  # ObjectId를 문자열로 변환
    #     return ret
    
class OfflinePopupStoreSimpleSerializer(serializers.Serializer):
    # id = serializers.CharField(source='_id',max_length=200)
    id = serializers.SerializerMethodField()
    title = serializers.CharField(max_length=200)
    location = LocationDictSerializer(required=False)
    description = serializers.ListField(child=serializers.CharField(), required=False)
    isSaved = serializers.SerializerMethodField(required=False)
    image = serializers.SerializerMethodField(required=False)
    # viewCount = serializers.IntegerField()
    viewCount = serializers.SerializerMethodField()
    
    def get_id(self, obj):
        try:
            id = str(obj.id)
        except:
            id = str(obj.get('_id'))
            
        return id
    
    def get_image(self, obj):
        
        db = MongoDBClient.get_database('poppingmongo')
        fs = gridfs.GridFS(db)
        
        try:
            img_id = str(obj.image[0].grid_id)
        except:
            img_id = str(obj.get('image')[0])
            
        cache_key = f"popup_image_{img_id}"
        encoded_img = cache.get(cache_key)
        
        if not encoded_img:
            file = fs.get(ObjectId(img_id))
            
            encoded_img = base64.b64encode(file.read()).decode('utf-8')
            cache.set(cache_key, encoded_img, timeout=60*60*24)  # 24시간 동안 캐시
            
        return encoded_img
    
    def get_viewCount(self,obj):
        try:
            viewCount = obj.viewCount
        except:
            viewCount = obj.get('viewCount')
            
        return viewCount
    
    def get_isSaved(self, obj):
        user: User = self.context.get('user')
        try:
            return str(obj.id) in user.savedPopup
        except:
            return False
        
class OfflinePopupStoreSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200)
    brandName = serializers.CharField(max_length=200)
    title = serializers.CharField(max_length=200)
    location = LocationDictSerializer(required=False)
    date = DateDictSerializer(required=False)
    tag = serializers.ListField()
    openTime = serializers.ListField(child=serializers.JSONField(), required=False)
    description = serializers.ListField(child=serializers.CharField(), required=False)
    isSaved = serializers.SerializerMethodField(required=False)
    image = serializers.SerializerMethodField(required=False)
    homepage = serializers.CharField(max_length=200)
    sns = serializers.CharField(max_length=200)
    viewCount = serializers.SerializerMethodField()
    saveCount = serializers.SerializerMethodField()

    def get_image(self, obj):
        db = MongoDBClient.get_database('poppingmongo')
        fs = gridfs.GridFS(db)
        
        images = []
        
        for img in obj.image:
            img_id = str(img.grid_id)
                
            cache_key = f"popup_image_{img_id}"
            encoded_img = cache.get(cache_key)
            
            if not encoded_img:
                file = fs.get(img.grid_id)
                
                encoded_img = base64.b64encode(file.read()).decode('utf-8')
                cache.set(cache_key, encoded_img, timeout=60*60*24)  # 24시간 동안 캐시
                
            images.append(encoded_img) 
        
        return images
    
    def get_isSaved(self, obj):
        user: User = self.context.get('user')
        try:
            return str(obj.id) in user.savedPopup
        except:
            return False
    
    def get_viewCount(self,obj):
        try:
            viewCount = obj.viewCount
        except:
            viewCount = obj.get('viewCount')
            
        return viewCount

    def get_saveCount(self, obj):
        try:
            saveCount = obj.saveCount
        except:
            saveCount = obj.get('saveCount')

        return saveCount
        
class MainPopupSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    title = serializers.CharField(max_length=200)
    location = LocationDictSerializer(required=False)
    image = serializers.SerializerMethodField(required=False)

    def get_id(self, obj):
        try:
            id = str(obj.id)
        except:
            id = str(obj.get('_id'))
            
        return id
    
    def get_image(self, obj):
        
        db = MongoDBClient.get_database('poppingmongo')
        fs = gridfs.GridFS(db)
        
        try:
            img_id = str(obj.image[0].grid_id)
        except:
            img_id = str(obj.get('image')[0])
            
        cache_key = f"popup_image_{img_id}"
        encoded_img = cache.get(cache_key)
        
        if not encoded_img:
            file = fs.get(ObjectId(img_id))
            
            encoded_img = base64.b64encode(file.read()).decode('utf-8')
            cache.set(cache_key, encoded_img, timeout=60*60*24)  # 24시간 동안 캐시
            
        return encoded_img

    