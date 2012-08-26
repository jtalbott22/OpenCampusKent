from ebpub.db.models import NewsItem, Schema
from django.contrib.gis.geos import Point
import datetime
from ksublock.scrapers.yelp import YelpApi
schema = Schema.objects.get(slug='campus-event')
yelpAxes = YelpApi('nRv6gPdCwEopk82FK_cwcA','g8VQ_wr3wgWspFEYFaW-S0Z4dBI','rS-u-TkmWViYGmblyi7M4pmCwIpLbdwD','H4xrxatP9OCuGt2gnQxmpELnUXc')
params = {'deals_filter' : False,  'bounds' : " 41.0834917675, -81.39382852783203|41.206297513, -81.30878448486328", 'limit' : '20'}
response = yelpAxes.search(params)


newsItem = NewsItem()
for yelpPost in response:
 print yelpPost

