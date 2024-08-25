import mongoengine as me

# Create your models here.
class LocationDict(me.EmbeddedDocument):
    meta = {
        'indexes': [
            {'fields': ['$geoData'], 'type': '2dsphere'}
        ]
    }
    address = me.StringField(required=True)
    placeName = me.StringField(required=False)
    geoData = me.PointField(required=False)  # GeoJSON 포인트 형식의 위치 정보

class OfflinePopup(me.Document):
    meta = {
        'collection': 'OfflinePopup',
    }
    brandName = me.StringField(required=True)
    title = me.StringField(required=True)
    url = me.StringField(required=True)
    date = me.DictField(required=True)
    location = me.EmbeddedDocumentField(LocationDict)
    tag = me.ListField(me.StringField(),required=False)
    badge = me.ListField(me.StringField(),required=False)
    openTime = me.ListField(me.DictField(),required=False)
    description = me.ListField(me.StringField(),required=False)
    image = me.ListField(me.ImageField(),required=False)
    homepage = me.StringField(required=False)
    sns = me.StringField(required=False)
    status = me.IntField(required=False, default=0)
    viewCount = me.IntField(default=0)
    # caption = me.StringField(required=False)

class Place(me.Document):
    meta = {
        'collection': 'Place',
        'indexes': [
            {'fields': ['$geoData'], 'type': '2dsphere'},
            {'fields': ['gradePoint', 'tags']}  # 또 다른 복합 인덱스
        ]
    }
    option = me.StringField(required=True) # 맛집:food, 카페:cafe
    title = me.StringField()
    bestMenu = me.ListField(me.StringField(), required=True)  
    gradePoint = me.FloatField(required=True)
    loadAddr = me.StringField()
    numberAddr = me.StringField()
    telNumber = me.StringField(unique=True)
    tags = me.ListField(me.StringField(),required=True)
    charTag = me.ListField(me.StringField(),required=True)
    geoData = me.PointField(required=False)  # GeoJSON 포인트 형식의 위치 정보
    image = me.ImageField(required=False)


