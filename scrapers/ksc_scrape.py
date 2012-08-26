#!/usr/bin/env python
# encoding: utf-8

#
# Filename: ksc_scrape.py
#
# Author: Matt Gates
#
# Description: Downloads calendar entries from RSS feed at ecalendar.kent.edu and updates the database
#

from django.conf import settings
from django.contrib.gis.geos import Point
from ebpub.db.models import NewsItem, Schema
from ebpub.utils.script_utils import add_verbosity_options, setup_logging_from_opts
from optparse import OptionParser
from BeautifulSoup import BeautifulSoup
import dateutil.parser
import ebdata.retrieval.log  # sets up base handlers.
import logging
import pytz
import sys, feedparser, datetime
from ebdata.retrieval.utils import convert_entities
from ebpub.streets.models import Place, PlaceType, PlaceSynonym
from ebdata.nlp import places

logger = logging.getLogger('eb.retrieval.ksc.events')
local_tz = pytz.timezone(settings.TIME_ZONE)

#
#
# This function needs to be converted to something that utilizes BeautifulSoup
#
## Usage:
#
# var = "My lazy dog runs everywhere"
# foo(var, 'My', 'everywhere')
#
## Output:
#
# lazy dog runs
#
#


def foo(s, leader, trailer):
	end_of_leader = s.index(leader) + len(leader)
	start_of_trailer = s.index(trailer, end_of_leader)
	return s[end_of_leader:start_of_trailer]

class KSUStudentProgrammingScraper(object):

	#
	#
	# Defines the RSS feed URL ; This one retrieves only 4 entries
	#
	#
	url = "http://ecalendar.kent.edu/RSSSyndicator.aspx?category=4-0,21-0,19-0,18-0,9-0&location=1-21-0,1-133-0,1-83-0&binary=Y&number=4"

	def __init__(self, schema_slug='news'):
		try:
			self.schema = Schema.objects.get(slug=schema_slug)
		except Schema.DoesNotExist:
			logger.error("Schema (%s): DoesNotExist" % schema_slug)
			sys.exit(1)

	def update(self):

		#
		#
		# Download Calendar RSS feed and update database
		#
		#

		logger.info("Starting KSUStudentProgrammingScraper")

		feed = feedparser.parse(self.url)
		seencount = addcount = updatecount = 0
		for entry in feed.entries:

			seencount += 1
			title = convert_entities(entry.title)
			title = foo(title, '', ' (')
			try:
				item = NewsItem.objects.get(title=title,
											schema__id=self.schema.id)
				status = "updated"
			except NewsItem.DoesNotExist:
				item = NewsItem()
				status = "added"
			except NewsItem.MultipleObjectsReturned:
				logger.warn("Multiple entries matched title %r, event titles are not unique?" % title)
				continue
			try:

				#
				#
				# The actual rss feed elements are grabbed here
				#
				#

				itm_description = entry.description

				soup = BeautifulSoup(foo(itm_description,"</table><br />","<br /><br />"))
				locations = soup.findAll(text=True)
				location = locations[0].strip()
				place_grabber = places.place_grabber()
				grab_results = place_grabber(location)
				try:
					item.location = Place.objects.get(pretty_name=grab_results[0][2]).location
					item.location_name = Place.objects.get(pretty_name=grab_results[0][2]).pretty_name
				except:
					item.location = PlaceSynonym.objects.get(pretty_name=grab_results[0][2]).place.location
					item.location_name = PlaceSynonym.objects.get(pretty_name=grab_results[0][2]).place.pretty_name

				try:
					item.attributes['room'] = locations[1].strip().replace("Room: ","")
				except Exception as e:
					logger.info("Tried saving item.room, error: %s" % e)

				item.schema = self.schema
				item.title = title

				soup = BeautifulSoup(foo(itm_description,"<br /><br />","</td></tr>"))
				item.description = soup.findAll(text=True)
				item.description = item.description[0].strip()

				item.url = entry.link

				start_t = foo(itm_description,"Start Time:</b>&nbsp;</td><td>","</td>")
				start_t = dateutil.parser.parse(start_t)

				end_t = foo(itm_description,"End Time:</b>&nbsp;</td><td>","</td>")
				end_t = dateutil.parser.parse(end_t)

				end_dt = foo(itm_description,"End Date:</b>&nbsp;</td><td>","</td>")
				end_dt = dateutil.parser.parse(end_dt)

				item.item_date = dateutil.parser.parse(entry.category)
				item.pub_date = datetime.datetime(*entry.updated_parsed[:6])

				item.attributes['start-time'] = start_t.time()
				item.attributes['end-time'] = end_t.time()

				item.save()

				if status == 'added':
					addcount += 1
				else:
					updatecount += 1
				logger.info("%s: %s" % (status, item.title))
			except Exception as e:
				logger.exception("unexpected error: %s" % e)
		logger.info("KSUStudentProgrammingScraper finished: %d added, %d updated of %s total" % (addcount, updatecount, seencount))

def main(argv=None):
	if argv is None:
		argv = sys.argv[1:]
	optparser = OptionParser()
	add_verbosity_options(optparser)
	opts, args = optparser.parse_args(argv)
	setup_logging_from_opts(opts, logger)
	KSUStudentProgrammingScraper().update()

if __name__ == '__main__':
	sys.exit(main())