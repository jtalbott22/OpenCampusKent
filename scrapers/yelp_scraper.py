from ebpub.db.models import NewsItem, Schema
from django.contrib.gis.geos import Point
from datetime import datetime
from ksublock.scrapers.yelp import YelpApi
from django.conf import settings


schema = Schema.objects.get(slug='reviews')
yelpAxes = YelpApi(settings.YELP_CONSUMER, 
		   settings.YELP_CONSUMER_SECRET, 
		   settings.YELP_TOKEN, 
		   settings.YELP_TOKEN_SECRET)

params = {'deals_filter' : False, 
	  'bounds' : " 41.0834917675, -81.39382852783203|41.206297513, -81.30878448486328",
	  'limit' : '20'}

response = yelpAxes.search(params)


for yelpPost in response['businesses']:
	newsItem = NewsItem()
	newsItem.schema = schema
	newsItem.description = yelpPost['snippet_text']
	newsItem.rating = yelpPost['rating']

	newsItem.url = yelpPost['url']
	newsItem.title = yelpPost['name']
	newsItem.item_date = datetime.now()
	newsItem.pub_date = datetime.now()
	newsItem.location_name = 'Kent'
	newsItem.location = Point((float (yelpPost['location']['coordinate']['longitude']),
			float (yelpPost['location']['coordinate']['latitude'])))
	newsItem.save()

