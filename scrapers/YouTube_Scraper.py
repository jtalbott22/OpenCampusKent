#!/usr/bin/env python
# encoding: utf-8
#
# Filename: YouTube_Scraper.py
#
# Author: Josh Talbott
#
# Description: Uses YouTubeAPI.py to pull queries from YouTube and update the database
#
from ksublock.scrapers.YouTubeAPI import YouTubeAPI
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
import string
import logging
import pytz
import sys, datetime
import dateutil.parser

logger = logging.getLogger('eb.retrieval.video.events')
local_tz = pytz.timezone(settings.TIME_ZONE)

class YouTubeScraper(object):
        def __init__(self, schema_slug='videos'):
                try:
                        self.schema = Schema.objects.get(slug=schema_slug)
                except Schema.DoesNotExist:
                        logger.error("Schema (%s): DoesNotExist" % schema_slug)
                        sys.exit(1)

        def update(self, searchTerm, searchOffset):
                youtubeAPI = YouTubeAPI()
                numentries = 50 #How many results do we want the API to return
                logger.info("Starting YouTube_Scraper")
                response = youtubeAPI.runQuery(searchTerm, numentries, searchOffset)
                seencount = addcount = updatecount = 0
                if response:
                                for entry in response:
                                                seencount += 1
                                                count = 0
                                                while count != 9:
							if 'ns'+ str(count) + ':title' in entry:
								if entry['ns'+ str(count) + ':title'] != '':
									title = entry['ns'+ str(count) + ':title']
									count += 1
                                                        	else:
									logger.info("Skipping, as title is empty.")
									continue
							else:
								count += 1
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
                                                                        if entry['ns'+ str(count) + ':description'] != '':
                                                                                newsItem.description = entry['ns'+ str(count) + ':description']
                                                                                break
                                                                        else:
                                                                              logger.info("Skipping %r as description is empty." % (title))
                                                                              continue
                                                                else:
                                                                        count += 1
                                                        newsItem.url = entry['ns0:link']
                                                        count = 0
                                                        while count != 9:
                                                                if 'ns'+ str(count) + ':title' in entry:
                                                                        if entry['ns'+ str(count) + ':title'] != '':
                                                                                newsItem.title = entry['ns'+ str(count) + ':title']
                                                                                count += 1
                                                                        else:
                                                                                logger.info("Skipping, as title is empty.")
                                                                                continue
                                                                else:
                                                                        count += 1
                                                        # newsItem.item_date = datetime.datetime.now()
                                                        count = 0
                                                        while count != 9:
                                                                if 'ns'+ str(count) + ':published' in entry:
                                                                        yt_timedate = string.split(entry['ns'+ str(count) + ':published'],'T')
                                                                        break
                                                                else:
                                                                        count += 1
                                                        date = yt_timedate[0]
                                                        time = string.split(yt_timedate[1],'Z')
                                                        formatted = date
							#date + " " + time[0] + "000" #Used to include timestamps
                                                        newsItem.pub_date = datetime.datetime.now()
                                                        newsItem.item_date = formatted.encode( "utf-8" )
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
                                                                        logger.info("Skipping %r as %s,%s is out of bounds" % (_short_title, y, x))
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

                                                        attributes_ = {}
                                                        attributes_['photo_href'] = entry['ns0:thumb']
                                                        attributes_['videoID'] = entry['ns0:video_id']
							attributes_['searchTerm'] = searchTerm
    
                                                        newsItem.save()
                                                        newsItem.attributes = attributes_
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
        for item in settings.YOUTUBE_KEYWORDS:
			YouTubeScraper().update(item,'1')
			YouTubeScraper().update(item,'51')
			YouTubeScraper().update(item,'101')
			YouTubeScraper().update(item,'151')

if __name__ == '__main__':
        sys.exit(main())
