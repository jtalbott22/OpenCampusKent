#!/usr/bin/env python

"""A quick-hack news scraper script for Kent student center programming; consumes RSS feeds for events.
"""
from ebdata.nlp.addresses import parse_addresses
from ebdata.retrieval.scrapers.list_detail import RssListDetailScraper
from ebdata.retrieval.scrapers.newsitem_list_detail import NewsItemListDetailScraper
from ebdata.textmining.treeutils import text_from_html
from ebpub.db.models import NewsItem
from ebpub.geocoder import SmartGeocoder
from ebpub.geocoder.base import GeocodingException
from ebpub.utils.logutils import log_exception
from ebdata.nlp import places
import logging
import datetime
from ebpub.db.models import *
from ebpub.streets.models import Place, PlaceType, PlaceSynonym
from django.core.exceptions import ObjectDoesNotExist

class KSCScraper(RssListDetailScraper, NewsItemListDetailScraper):

    schema_slugs = ('events',)
    has_detail = False

    def list_pages(self):
        # This gets called to iterate over pages containing lists of items.
        # We just have the one page.
        url = 'http://ecalendar.kent.edu/RSSSyndicator.aspx?category=4-0,21-0,19-0,18-0,9-0&location=1-21-0,1-133-0,1-83-0&binary=Y&number=4'
        yield self.fetch_data(url)

    def existing_record(self, record):
        # This gets called to see if we already have a matching NewsItem.
        url = record['link']
        qs = NewsItem.objects.filter(schema__id=self.schema.id, url=url)
        try:
            return qs[0]
        except IndexError:
            return None

    def save(self, old_record, list_record, detail_record):
        # This gets called once all parsing and cleanup is done.
        # It looks a lot like our 'expedient hack' code above.

        # We can ignore detail_record since has_detail is False.

        date = datetime.date(*list_record['updated_parsed'][:3])
        description = text_from_html(list_record['summary'])

        # This feed doesn't provide geographic data; we'll try to
        # extract addresses from the text, and stop on the first
        # one that successfully geocodes.
        # First we'll need some suitable text; throw away HTML tags.
       # full_description = list_record['content'][0]['value']
       # full_description = text_from_html(full_description)
        grabber =  places.place_grabber()
	print  description + '\n'
	print list_record['summary']
        addrs = grabber(list_record['summary'])
       # printing articles title for debugging
       # print list_record['title']
	print addrs
        if not addrs:
            addrs = grabber(list_record['title'])
            if not addrs:
                self.logger.info("no addresses found")
                return

        location = None
        location_name = u''
        block = None
        # Ready to geocode. If we had one location_name to try,
        # this could be done automatically in create_or_update(), but
        # we have multiple possible location_names.
        for l, r, name in addrs:
            #addr = addr.strip()
            
            #aPlace = Place.objects.get(pretty_name = name)
            
		
            try:
                aPlace = Place.objects.get(pretty_name = name)
                location = aPlace.location
            except ObjectDoesNotExist:
                newslocation = PlaceSynonym.objects.get(pretty_name = name).place.location
	        print newslocation
                location = newslocation	
           # except GeocodingException:
            #    log_exception(level=logging.DEBUG)
             #   continue
            location_name = name
           # block = location['block']
           # location = location['point']
            break
        if location is None:
            self.logger.info("no addresses geocoded in %r" % list_record['title'])
            return
	print location
        kwargs = dict(item_date=date,
                      location=location,
                      location_name=location_name,
                      description=description,
                      title=list_record['title'],
                      url=list_record['link'],
                      )
        attributes = None
        self.create_or_update(old_record, attributes, **kwargs)


if __name__ == "__main__":
        import sys
        from ebpub.utils.script_utils import add_verbosity_options, setup_logging_from_opts
        from optparse import OptionParser
#       if argv is None:
#           argv = sys.argv[1:]
        optparser = OptionParser()
        add_verbosity_options(optparser)
        scraper = KSCScraper()
#       opts, args = optparser.parse_args(argv)
#       setup_logging_from_opts(opts, scraper.logger)
        # During testing, do this instead:
        # scraper.display_data()
        scraper.update()



