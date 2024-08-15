from rest_framework import serializers
from .models import PopupStore
from user.models import User

class LocationDictSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=200)
    placeName = serializers.CharField(max_length=100)
    geoData = serializers.JSONField(required=False)

class PopupStoreSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200)
    title = serializers.CharField(max_length=200)
    location = LocationDictSerializer(required=False)
    startDate = serializers.DateTimeField(required=False)
    endDate = serializers.DateTimeField(required=False)
    openTime = serializers.ListField(child=serializers.CharField(), required=False)
    event = serializers.ListField(child=serializers.CharField(), required=False)
    isSaved = serializers.SerializerMethodField()
    view = serializers.IntegerField()
    saved = serializers.IntegerField()

    def get_isSaved(self, obj):
        user: User = self.context.get('user')
        return str(obj.id) in user.savedPopup


class PlaceSerializer(serializers.Serializer):
    # id = serializers.CharField(max_length=200)
    # id = serializers.CharField(source='_id', read_only=True)
    title = serializers.CharField(max_length=200)
    bestMenu = serializers.ListField(child=serializers.CharField(), required=False)
    gradePoint = serializers.IntegerField()
    loadAddr = serializers.CharField(max_length=200)
    numberAddr = serializers.CharField(max_length=200)
    telNumber = serializers.CharField(max_length=200)
    option = serializers.CharField(max_length=200)
    charTag = serializers.ListField(child=serializers.CharField(), required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    geoData = serializers.JSONField(required=False)
    
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     ret['id'] = str(ret['id'])  # ObjectId를 문자열로 변환
    #     return ret
    