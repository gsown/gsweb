from django.shortcuts import render
from ljdata.models import HouseInfo,AreaList,HouseBrowse
from django.core.paginator import Paginator
from mongoengine import connect
connect('lianjia', host = '127.0.0.1', port = 27017)

# Create your views here.
start_date = ['2010-01-01','2011-01-01','2012-01-01','2013-01-01','2014-01-01','2015-01-01','2016-01-01','2017-01-01']
end_date = ['2010-12-31','2011-12-31','2012-12-31','2013-12-31','2014-12-31','2015-12-31','2016-12-31','2017-12-31']
annual_list = ['2010年','2011年','2012年','2013年','2014年','2015年','2016年','2017年']
### ----------------------大连二手房各区域总成交量-------------------------------------------------------------------------#
pipeline23 = [
    {'$project':{'_id':0, 'area':1}},
    {'$group':{'_id':'$area', 'sum':{'$sum':1}}},
    {'$sort':{'sum':-1}}
]
pipeline22 = [
    {'$project':{'_id':0, 'area':1}},
    {'$group':{'_id':{'$slice':['$area',0,1]}, 'sum':{'$sum':1}}},
    {'$sort':{'sum':-1}}
]
def get_area_sum():
    for i in HouseInfo._get_collection().aggregate(pipeline22):
        data = {
            'name':i['_id'][0],
            'y':i['sum'],
            'drilldown':i['_id'][0]
        }
        yield data


def detail_info():
    for im in get_area_sum():
        list1 = []
        for i in HouseInfo._get_collection().aggregate(pipeline23):
            if i['_id'][0] == im['name']:
                list1.append([i['_id'][1],i['sum']])
            else:
                pass
        data = {
            # 'name':im['name'],
            'id':im['name'],
            'data':list1
        }
        yield data
all_area = [i for i in get_area_sum()]
detial = [ i for i in detail_info()]
# --------------------------------------------------------------------------------------------------------------------

#---------------------------大连各区域各年度二手房数量统计------------------------------------------------------------------
def get_area_data():
    area_list1 = []
    for i in AreaList.objects():
        if i['area'][0] in area_list1:
            pass
        else:
            area_list1.append(i['area'][0])
    for im in area_list1:
        area_year_posts = []
        for a, b in zip(start_date, end_date):
            pipeline = [
                {'$match': {'saleDate': {'$gte': a, '$lte': b}}},
                {'$project': {'_id': 0, 'area': 1}},
            ]
            sum = 0
            for i in HouseInfo._get_collection().aggregate(pipeline):
                if i['area'][0] == im:
                    sum += 1
                else:
                    pass
            if sum == 0:
                area_year_posts.append('null')
            else:
                area_year_posts.append(sum)
        data = {
            'name': im,
            'data': area_year_posts,

        }
        yield data
annual_num_data = [i for i in get_area_data()]
# -----------------------------------------------------------------------------------------------------------

# -------------------成交量前十--------------------------------------------------------------------------------
pipeline = [
    {'$project':{'_id':0, 'area':1}},
    {'$group':{'_id':'$area','sum':{'$sum':1}}},
    {'$sort':{'sum':-1}},
    {'$limit':10}
]
def top_ten():
    listt = []
    for i in HouseInfo._get_collection().aggregate(pipeline):
        listt.append([i['_id'][1], i['sum']])
    data = {
        'name':'成交量',
        'data':listt,
        }
    yield data
top_ten_data = [data for data in top_ten()]
# ----------------------------------------------------------------------------------------------------------------

# --------------------------------------大连总成交量前10区域年度房价统计----------------------------------------------
def get_top_ten_avg_price():
    for im in HouseInfo._get_collection().aggregate([{'$project':{'_id':0, 'area':1}},{'$group':{'_id':'$area','sum':{'$sum':1}}},{'$sort':{'sum':-1}},{'$limit':10}]):
        area_year_posts = []
        for a,b in zip(start_date,end_date):
            pipeline = [
                {'$project':{'_id':0, 'area':1, 'unitPrice':1, 'saleDate':1}},
                {'$match':{'saleDate':{'$gte':a,'$lte':b}}},
                {'$group':{'_id':'$area','avg_price':{'$avg':'$unitPrice'}}}
                ]
            sum = 0
            for i in HouseInfo._get_collection().aggregate(pipeline):

                if i['_id'][1] == im['_id'][1]:
                    area_year_posts.append(i['avg_price'])
                    sum += 1
                else:
                    pass
            if sum == 0:
                area_year_posts.append('null')
            else:
                pass
        data = {
            'name': im['_id'][1],
            'data': area_year_posts,
        }
        yield data
top_ten_avg_price = [i for i in get_top_ten_avg_price()]
# ----------------------------------------------------------------------------------------------------------------

# --------------------------------------浏览量前200的房屋面积和价格分布----------------------------------------------
pipeline = [
    {'$project':{'_id':0,'price':1,'area':1,'spaceSize':1,'browse':1}},
    {'$sort':{'browse':-1}},
    {'$limit':200}
]

area_list1 = []
def get_total():
    for i in AreaList._get_collection().aggregate([{'$project':{'_id':0,'area':1}}]):
        if i['area'][0] in area_list1:
            pass
        else:
            area_list1.append(i['area'][0])
    for m in area_list1:
        list = []
        for i in HouseBrowse._get_collection().aggregate(pipeline):
            if i['area'][0] == m:
                list.append([i['spaceSize'],i['price']])
            else:
                pass
        if m == '沙河口':
            color = 'rgba(124,  181,  236, .5)'
        elif m == '甘井子':
            color = 'rgba(67, 67 ,72, .5)'
        elif m == '金州':
            color = 'rgba(144, 237, 125, .5)'
        elif m == '西岗':
            color = 'rgba(247, 163, 92, .5)'
        elif m == '中山':
            color = 'rgba(165, 0, 255, .5)'
        elif m == '高新园区':
            color = 'rgba(241, 92, 128, .5)'
        else:
            color = 'rgba(228, 211, 84, .5)'
        data = {
            'color': color,
            'name':m,
            'data':list
        }
        yield data
top_200 = [i for i in get_total()]
# ----------------------------------------------------------------------------------------------------------------

# --------------------------------------------
start_price = ['0','40','60','80','100','150','200']
end_price = ['40','60','80','100','150','200','10000']
limit = ['40万以下','40-60万','60-80万','80-100万','100-150万','150-200万','200万以上']
def get_proportion():
    for sp,ep,li in zip(start_price,end_price,limit):
        sum = 0
        for i in HouseInfo._get_collection().aggregate([{'$project':{'_id':0, 'price':1}}]):
            if int(sp) <= float(i['price'])  <= int(ep):
                sum += 1
            else:
                pass
        yield [li,sum]
pie_data = [i for i in get_proportion()]
# --------------------------------------------------------------------------------------------

def index(request):
    limit = 15
    house_info = HouseInfo.objects
    paginatior = Paginator(house_info,limit)
    page = request.GET.get('page',1)
    loaded = paginatior.page(page)
    context = {
        'HouseInfo':loaded,
        'counts': house_info.count(),
        'last_time': house_info.order_by('-dealDate').limit(1)
    }
    return render(request, "index.html", context)

def charts(request):
    context = {
        # 'all_area_series': all_area_series,
        'all_area': all_area,
        'detial': detial,
        'annual_num_data': annual_num_data,
        'top_ten_data': top_ten_data,
        'top_ten_avg_price': top_ten_avg_price,
        'top_200': top_200,
        'pie_data': pie_data,
    }
    return render(request, 'charts.html', context)

def about(request):
    return render(request, "about.html")
