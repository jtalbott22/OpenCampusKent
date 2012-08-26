"""
Copy this to settings.py, uncomment the various settings, and
edit them as desired.
"""

from ebpub.settings_default import *

########################
# CORE DJANGO SETTINGS #
########################

DEBUG = True
TIME_ZONE = 'US/Eastern'

PROJECT_DIR = os.path.normpath(os.path.dirname(__file__))
INSTALLED_APPS = ('ksublock', ) + INSTALLED_APPS
TEMPLATE_DIRS = (os.path.join(PROJECT_DIR, 'templates'), ) + TEMPLATE_DIRS
ROOT_URLCONF = 'ksublock.urls'

#
# Twitter Scraper Whitelist
#
# The businesses that are allowed to use the #kentdeals or #kentevents hashtags
#

TWITTER_WHITELIST = ['gfrommy', 'smitty2357', 'OpenCampusKent', 'jtalbott22']
TWITTER_DEALS_KEYWORDS = ['@TacoTantos','@Poppedstore','@KentRiverside','@sketchstudiok','@Zoupwerks','@evolsk8shop','@KentNatFoods','@LaroushKent','@McKayBricker','@treecitycoffee','@raysplacekent','@157Lounge','@KentStage','@CajunDaves','@WaterStTavern']


FLICKR_API_KEY = '9639817bc9240e3849b963094330b7f5'
FLICKR_API_SECRET = '152c23632b6674a0'
YELP_CONSUMER = 'nRv6gPdCwEopk82FK_cwcA'
YELP_CONSUMER_SECRET = 'g8VQ_wr3wgWspFEYFaW-S0Z4dBI'
YELP_TOKEN = 'rS-u-TkmWViYGmblyi7M4pmCwIpLbdwD'
YELP_TOKEN_SECRET = 'H4xrxatP9OCuGt2gnQxmpELnUXc'


FLICKR_KEYWORDS = ['Kent State University', 'Kent','bassmasta17']
YOUTUBE_KEYWORDS = ['Kent State University','Kent State Basketball','Kent State football','Kent State basketball','Kent State baseball','Kent State field hockey','Kent State ice hockey','Kent State gymnastics','Kent State sports','KSU Risman Plaza','KSU Manchester field','Painting the rock KSU','Front campus rock','KSU Vets','KSU esplanade','Downtown Kent','President Lefton','KSU Hub','Flash','Dix Stadium','Home Savings Plaza Kent','Campus Pointe','Kent black squirrel','Black squirrel radio','TV2 Kent State','TV2 KSU','Rathskeller','The Kent Stage','Acorn Alley','Acorn Alley 2','Acorn Alley II','Zoupwerks','Water Street Tavern','157 Lounge','The Zephyr','Zeph patio','Taco Tantos','KSU Ice Arena','Student Recreation and Wellness Center','Kent State SRWC','Scribbles coffee','Water Street Kent','Main Street Kent','KSU Fashion School','KSU Fashion Show','Rock the Runway','MACC','MAC Center','Rosies','Tri-Towers','Eastway','Golden Flashes','KSU Parking Services','KSU Library','KSU Book Store','The BURR','OpenCampusKent','OCKent','Mugs Kent','Ray\'s Place Kent','Acorn Alley Kent','Kent Dagorhir','Kent State Rugby','Kent State Football','Kent State baseball','Kent State field hockey','Kent State ice hockey','Kent State gymnastics','folk alley','wksu','Kent State USG','Kent State Hillel','Zephyr pub', 'kent state eastway','TheRecordPub', 'KentOhio360', 'KentStateTV', 'KentStateDodgeball', 'FlashCommunications', 'ISSSKentState', 'DSmithKent100', 'ExploreKent', 'ThatGayMagazine', 'TV2Kent', 'GoldenFlashesTV', 'FolkAlleydotcom', 'WKSURadio', 'CCIKent', 'TheKentOhio', 'StoddardsCustard', 'WKSUFreshair', 'spikydan1', 'Sportscornertv2', 'Kentstatesid', 'Foltzp9', 'Sportscaster17', 'KSUfood', 'KSUucm', 'KentStatelibraries', 'KentStateGymnastics', 'KSUmuseum']

DATABASES = {
    'default': {
        'NAME': 'openblock_ksublock',
        'USER': 'openblock',
        'PASSWORD': 'openblock',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'OPTIONS': {},
        'HOST': '',
        'PORT': '',
        'TEST_NAME': 'test_openblock',
    },
}

#########################
# CUSTOM EBPUB SETTINGS #
#########################

# The domain for your site.
EB_DOMAIN = 'opencampus.jmc.kent.edu'

# This is the short name for your city, e.g. "chicago".
SHORT_NAME = 'kent'

# Set both of these to distinct, secret strings that include two instances
# of '%s' each. Example: 'j8#%s%s' -- but don't use that, because it's not
# secret.  And don't check the result in to a public code repository
# or otherwise put it out in the open!
PASSWORD_CREATE_SALT = '2Lmj0B8MSMdt%s%s'
PASSWORD_RESET_SALT = '8DW7XmGrWaKl%s%s'

# You probably don't need to override this, the setting in settings.py
# should work out of the box.
#EB_MEDIA_ROOT = '' # necessary for static media versioning.

EB_MEDIA_URL = '' # leave at '' for development

MAP_BASELAYER_TYPE = 'google.streets'
GOOGLE_API_KEY='AIzaSyA7cRm--IGuwsjxm4ohwFgobLYNgecQLwA'

# This is used as a "From:" in e-mails sent to users.
GENERIC_EMAIL_SENDER = 'openblock@' + EB_DOMAIN

# Filesystem location of scraper log.
SCRAPER_LOGFILE_NAME = '/tmp/scraperlog_ksublock'

# If this cookie is set with the given value, then the site will give the user
# staff privileges (including the ability to view non-public schemas).
STAFF_COOKIE_NAME = 'obstaff_ksublock'
STAFF_COOKIE_VALUE = 'l6LBBzgVHkB3'

# What LocationType to redirect to when viewing /locations.
DEFAULT_LOCTYPE_SLUG='zipcodes'

# What kinds of news to show on the homepage.
# This is one or more Schema slugs.
HOMEPAGE_DEFAULT_NEWSTYPES = [u'news-articles']

# How many days of news to show on the homepage, place detail view,
# and elsewhere.
DEFAULT_DAYS = 7

# Where to center citywide maps, eg. on homepage.
DEFAULT_MAP_CENTER_LON = -81.34243
DEFAULT_MAP_CENTER_LAT = 41.146911
DEFAULT_MAP_ZOOM = 15

# Edit this if you want to control where
# scraper scripts will put their HTTP cache.
# (Warning, don't put it in a directory encrypted with ecryptfs
# or you'll likely have "File name too long" errors.)
HTTP_CACHE = '/tmp/openblock_scraper_cache_ksublock'

# Metros. You almost certainly only want one dictionary in this list.
# See the configuration docs for more info.
METRO_LIST = (
    {
        # Extent of the region, as a longitude/latitude bounding box.
                'extent': ( -81.39382852783203, 41.0834917675, -81.30878448486328, 41.206297513),


        # Whether this region should be displayed to the public.
        'is_public': True,

        # Set this to True if the region has multiple cities.
        # You will also need to set 'city_location_type'.
        'multiple_cities': False,

        # The major city in the region.
        'city_name': 'Kent',

        # The SHORT_NAME in the settings file.
        'short_name': SHORT_NAME,

        # The name of the region, as opposed to the city (e.g., "Miami-Dade" instead of "Miami").
        'metro_name': 'Kent',

        # USPS abbreviation for the state.
        'state': 'OH',

        # Full name of state.
        'state_name': 'Ohio',

        # Time zone, as required by Django's TIME_ZONE setting.
        'time_zone': TIME_ZONE,

        # Slug of an ebpub.db.LocationType that represents cities.
        # Only needed if multiple_cities = True.
        'city_location_type': None,
    },
)

CACHES = {
    # Use whatever Django cache backend you like;
    # FileBasedCache is a reasonable choice for low-budget, memory-constrained
    # hosting environments.
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/ksublock_cache'
          # # Use this to disable caching.
        #'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

##################
# MEDIA
##################

# For local development you might try this:
#JQUERY_URL = '/media/js/jquery.js'
JQUERY_URL = 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js'

if DEBUG:
    for _name in required_settings:
        if not _name in globals():
            raise NameError("Required setting %r was not defined in settings.py or settings_default.py" % _name)
