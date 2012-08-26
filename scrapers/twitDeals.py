#!/usr/bin/env python
# encoding: utf-8

#
# Filename: twitDeals.py
#
# Author: Matt Gates
#
# Description: Finds deals from Twitter !
#

from django.conf import settings
from django.contrib.gis.geos import Point
from ebpub.db.models import NewsItem, Schema
from ebpub.utils.script_utils import add_verbosity_options, setup_logging_from_opts
from optparse import OptionParser
from BeautifulSoup import BeautifulSoup
import dateutil.parser
import re
import ebdata.retrieval.log  # sets up base handlers.
import logging
import pytz
import sys, feedparser, datetime
import simplejson as json
import urllib2
import urllib
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

class TwitterScraper(object):

	#
	#
	# Twitter search API Parameters
	#
	#

	# Twitter Search API URL
	url = "http://search.twitter.com/search.json"

	# Hashtag to search for UPDATE!! LOOP OVER A LIST OF HASHTAGS IN SETTINGS.PY
	#hashtag = "#cajundaves"  

	# Allowed Twitter usernames, taken from settings.py
	allowed_users = settings.TWITTER_WHITELIST

	# Number of tweets to return
	tweets = "15"

	# 15 miles within KSU SC
	geocode = "41.148179,-81.342614,15mi"

	# Whether to include entities. Used so we can grab media, urls, hashtags, etc
	include_entities = "true"

	# Regex expression to match a date. MMDDYY
	re1='((?:[0]?[1-9]|[1][012])[-:\\/.](?:(?:[0-2]?\\d{1})|(?:[3][01]{1}))[-:\\/.](?:(?:\\d{1}\\d{1})))(?![\\d])'	# MMDDYY 1

	def __init__(self, schema_slug='deals'):
		try:
			self.schema = Schema.objects.get(slug=schema_slug)
		except Schema.DoesNotExist:
			logger.error("Schema (%s): DoesNotExist" % schema_slug)
			sys.exit(1)

	def search_twitter(self, hashtag):
		if not hashtag:
			raise Exception('No search hashtag specified - search halted')

		encoded_hashtag = urllib.quote(hashtag)
		self.request_url = "%s?q=%s&include_entities=%s&rpp=%s" % (self.url, encoded_hashtag, self.include_entities, self.tweets)

		return self.send_request()

	def send_request(self):
		try:
			conn = urllib2.urlopen(self.request_url, None)
			try:
				response = json.loads(conn.read())
			finally:
				conn.close()
		except urllib2.HTTPError, error:
			raise Exception('Wot happen? %s' % error)

		return response

	def update(self, hashtagItem):

		#
		#
		# Grab the Twitter feeds and start saving
		#
		#

		logger.info("Starting TwitterScraper")
		response = self.search_twitter(hashtagItem)
		seencount = addcount = updatecount = 0
		for entry in response['results']:
			seencount += 1
			title = entry['text'].replace('RT ','')
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
				# The actual Twitter return results are grabbed here
				#
				#

				if any(entry['from_user']) :
					item.schema = self.schema
					item.title = title
					item.description = entry['text'].replace('RT ','')
				#	item.location_name = entry['location']
					item.location_name = 'student center'

					item.photo_href = entry['profile_image_url']

					try :
						item.url = ("https://twitter.com/#!/%s/status/%s" % (entry['from_user'], entry['id_str']))
					except :
						print "No url"

					rg = re.compile(self.re1,re.IGNORECASE|re.DOTALL)
					m = rg.search(item.description)
					if m:
						mmddyy1=m.group(1)
						print "("+mmddyy1+")"+"\n"
					else :
						mmddyy1 = entry['created_at']

					item.item_date = dateutil.parser.parse(mmddyy1)
					item.pub_date = datetime.datetime.now()

					# print entry['entities']['hashtags']
					# print entry['location']

					item.save()
					item.attributes = {'photo_href' : entry['profile_image_url'], 'author' : entry['entities']['user_mentions'][0]['screen_name'] }
					item.save()

					if status == 'added':
						addcount += 1
					else:
						updatecount += 1
					logger.info("%s: %s" % (status, item.title))
			except Exception as e:
				logger.exception("unexpected error: %s" % e)
		logger.info("TwitterScraper finished: %d added, %d updated of %s total" % (addcount, updatecount, seencount))

def main(argv=None):
	if argv is None:
		argv = sys.argv[1:]
	optparser = OptionParser()
	add_verbosity_options(optparser)
	opts, args = optparser.parse_args(argv)
	setup_logging_from_opts(opts, logger)
	for item in settings.TWITTER_DEALS_KEYWORDS:
			TwitterScraper().update(item)

if __name__ == '__main__':
	sys.exit(main())
