#!/usr/bin/env python
# encoding: utf-8
#
# Filename: Yelp_Scraper.py
#
# Author: Kevin Donovan
#
# Description: Scrapes restaurant reviews from Yelp.com
#

from ebpub.db.models import NewsItem, Schema
from django.contrib.gis.geos import Point
from ebdata.nlp.addresses import parse_addresses
from ebpub.db.models import NewsItem, Schema
from ebpub.geocoder import SmartGeocoder
from ebpub.geocoder.base import GeocodingException
from ebpub.utils.logutils import log_exception
from ebpub.utils.geodjango import intersects_metro_bbox
from django.conf import settings
from ebpub.utils.script_utils import add_verbosity_options, setup_logging_from_opts
from optparse import OptionParser
from ksublock.scrapers.yelp import YelpApi
import string
import logging
import pytz
import sys, datetime
import dateutil.parser

logger = logging.getLogger('eb.retrieval.restaurant.reviews')
local_tz = pytz.timezone(settings.TIME_ZONE)

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


class YelpScraper(object):
        def __init__(self, schema_slug='reviews'):
                try:
                        self.schema = Schema.objects.get(slug=schema_slug)
                except Schema.DoesNotExist:
                        logger.error("Schema (%s): DoesNotExist" % schema_slug)
                        sys.exit(1)

        def update(self):
		yelp = YelpApi( settings.YELP_CONSUMER,
				settings.YELP_CONSUMER_SECRET,
				settings.YELP_TOKEN,
				settings.YELP_TOKEN_SECRET)
        	
	        numentries = 50 #How many results do we want the API to return
                logger.info("Starting Yelp")
                response = youtubeAPI.runQuery(searchTerm, numentries, searchOffset)
                seencount = addcount = updatecount = 0
                if response:
                                for entry in response:
                                                seencount += 1
                                                title = entry['ns0:title']
                                                try:
                                                        newsItem = NewsItem.objects.get(title=title,schema__id=self.schema.id)
                                                        status = "updated"
                                                except NewsItem.DoesNotExist:
                                                        newsItem = NewsItem()
                                                        status = "added"
                                                except NewsItem.MultipleObjectsReturned:
                                                        logger.warn("Multiple entries matched title %r, event titles are not unique?" % title)
                                                        continue
                                                try:
                                                        newsItem.schema = self.schema
                                                        count = 0
                                                        while count != 9:
                                                                if 'ns'+ str(count) + ':description' in entry:
                                                                        newsItem.description = entry['ns'+ str(count) + ':description']
                                                                        break
                                                                else:
                                                                        count += 1
                                                        newsItem.url = entry['ns0:link']
                                                        count = 0
                                                        while count != 9:
                                                                if 'ns'+ str(count) + ':title' in entry:
                                                                        newsItem.title = entry['ns'+ str(count) + ':title']
                                                                        break
                                                                else:
                                                                        count += 1
                                                        newsItem.item_date = datetime.datetime.now()
                                                        count = 0
                                                        while count != 9:
                                                                if 'ns'+ str(count) + ':updated' in entry:
                                                                        yt_timedate = string.split(entry['ns'+ str(count) + ':updated'],'T')
                                                                        break
                                                                else:
                                                                        count += 1
                                                        date = yt_timedate[0]
                                                        time = string.split(yt_timedate[1],'Z')
                                                        formatted = date + " " + time[0]
                                                        newsItem.pub_date = formatted
							_short_title = newsItem.title[:30] + '...'
                                                        #newsItem.location_name = 'Kent'
                                                        count = 0
                                                        while count != 9:
                                                                if 'ns'+ str(count) + ':pos' in entry:
                                                                        long_lat = string.split(entry['ns'+ str(count) + ':pos'])
                                                                        break
                                                                else:
                                                                        count += 1
                                                        newsItem.location = Point(float(long_lat[1]),float(long_lat[0]))
							x, y = float(long_lat[0]), float(long_lat[1])
                                                        if not intersects_metro_bbox(newsItem.location):
                                                                reversed_loc = Point((float(y), float(x)))
                                                                if intersects_metro_bbox(reversed_loc):
                                                                        logger.info(
                                                                                "Got points in apparently reverse order, flipping them")
                                                                        newsItem.location = reversed_loc
                                                                else:
                                                                        logger.info("Skipping %r as %s,%s is out of bounds" %
                                                                                (_short_title, y, x))
                                                                        continue
                                                        if not newsItem.location_name:
                                                                # Fall back to reverse-geocoding.
                                                                from ebpub.geocoder import reverse
                                                                try:
                                                                        block, distance = reverse.reverse_geocode(newsItem.location)
                                                                        logger.debug(" Reverse-geocoded point to %r" % block.pretty_name)
                                                                        newsItem.location_name = block.pretty_name
                                                                        newsItem.block = block
                                                                except reverse.ReverseGeocodeError:
                                                                        logger.info(" Skip, failed to reverse geocode %s for %r" % (newsItem.location.wkt, _short_title))
                                                                        continue

                                                        newsItem.save()
                                                        if status == 'added':
                                                                addcount += 1
                                                        else:
                                                                updatecount += 1
                                                        logger.info("%s: %s" % (status, newsItem.title))
                                                except Exception as e:
                                                        logger.exception("unexpected error: %s" % e)
                logger.info("YouTube_Scraper finished: %d added, %d updated of %s total" % (addcount, updatecount, seencount))

def main(argv=None):
        if argv is None:
                        argv = sys.argv[1:]
        optparser = OptionParser()
        add_verbosity_options(optparser)
        opts, args = optparser.parse_args(argv)
        setup_logging_from_opts(opts, logger)

	YelpScraper().update('asdf','151')

if __name__ == '__main__':
        sys.exit(main())

