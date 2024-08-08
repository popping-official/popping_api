from rest_framework import serializers
from .models import Maps

class MapsSerializer(serializers.Serializer):
    addrName = serializers.CharField(max_length=100)
    addr = serializers.CharField(max_length=200)
    geoAddr = serializers.SerializerMethodField()
    
    def get_geoAddr(self, obj):
        return (obj.addrName,00.1111111)