from django.db import models
import mongoengine as me

# Create your models here.

class Maps(me.Document):
    addrName = me.StringField(required=True, unique=True)
    addr = me.StringField(required=True, unique=True)
    
# class MapCategory(me.Document):
    