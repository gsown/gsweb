from django.db import models
from mongoengine import *
# from mongoengine import connect
# connect('lianjia', host = '127.0.0.1', port = 27017)
# Create your models here.

class HouseInfo(Document):
    saleDate = StringField()
    dealCycle = StringField()
    browse = StringField()
    see = StringField()
    unitPrice = FloatField()
    dealDate = StringField()
    follow = StringField()
    area = ListField(StringField())
    spaceSize = FloatField()
    url = StringField()
    price = FloatField()
    title = StringField()
    pattern = StringField()
    apartmentIntroduction = StringField()
    sealPoint = StringField()
    decorationDescription = StringField()
    tags = ListField(StringField())
    meta = {'collection': 'all_house_info'}

# for i in HouseInfo.objects[:1]:
#     print(i.title)
class AreaList(Document):
    area = ListField(StringField())
    url = StringField()
    where = StringField()
    sum = StringField()
    meta = {'collection': 'area_list'}

# for i in AreaList.objects[:1]:
#     print(i.where)

class HouseBrowse(Document):
    spaceSize = FloatField()
    browse = IntField()
    area = ListField(StringField())
    price = FloatField()
    mate = {'collection': 'house_browse'}
