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
from ebpub.db.models import Location, LocationSynonym
from ebpub.streets.models import Place, PlaceSynonym
class KentWiredScraper(RssListDetailScraper, NewsItemListDetailScraper):

    schema_slugs = ('kent-news',)
    has_detail = False

    def list_pages(self):
        # This gets called to iterate over pages containing lists of items.
        # We just have the one page.
        url = 'http://kentwired.com/component/option,com_ninjarsssyndicator/feed_id,2/format,raw/lang,en/'
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
        grabber = places.location_grabber()
 
        addrs = grabber(description)
       # printing articles title for debugging
       # print list_record['title']

        #if not addrs:
	#    addrs = grabber(list_record['title'])
 	#    if not addrs:
        #  	self.logger.info("no addresses found")
        #    	return

        location = None
        location_name = u''
        block = None

	
	grabber = places.place_grabber()
 
        addrs = grabber(description)

        #if not match is found article is assigned location of Kent State
        if not addrs:
            location_name  = "Kent State"
            locationSyn = LocationSynonym.objects.get(pretty_name = location_name)
            location = Location.objects.get(name = locationSyn.location).location
            self.logger.info("no matches for place found. Using Kent State default")
	else:	
            location = None
            location_name = u''
            block = None
	    
	    
	    #here we're checking the return results form the place grabber
	    #for mathces in the database. first Places are checked then PlaceSynonyms.
	    for l, r, name in addrs:
            #addr = addr.strip()
                try:
		    print name
                    place = Place.objects.get(pretty_name = name)
                    location = place.location
                except Place.DoesNotExist:
		    try:
                        place = PlaceSynonym.objects.get(pretty_name = name)
		        location = place.place.location
		    
		    except PlaceSynonym.DoesNotExist:
			self.logger.info("no addresses geocoded in %r" % list_record['title'])
			continue
                location_name = name
               # block = location['block']
               # location = location['point']
                break
            if location is None:
                self.logger.info("no addresses geocoded in %r" % list_record['title'])
                return



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
#	if argv is None:
#	    argv = sys.argv[1:]
	optparser = OptionParser()
	add_verbosity_options(optparser)
	scraper = KentWiredScraper()
#	opts, args = optparser.parse_args(argv)
#	setup_logging_from_opts(opts, scraper.logger)
	# During testing, do this instead:
	# scraper.display_data()
	scraper.update()
