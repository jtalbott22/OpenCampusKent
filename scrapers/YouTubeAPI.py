#YouTubeAPI.py written by Joshua A. Talbott
#Kent State University, JMC 2012

import gdata.youtube
import gdata.youtube.service
import sys
import xml.parsers.expat
import string
from BeautifulSoup import BeautifulSoup


#Example start from prompt: f = YouTubeAPI(['kent','state'])
# f.runQuery(30)
# f.parseXML() #returns a dictionary list

#We care about these fields in every entry of the dictionary list: ns0:title,
#ns6:description, ns0:updated, ns0:name, ns3:pos, ns0:link

#Call example: f.dictList[28]['ns0:title'] to get the title of the 29th entry.
#Substitute 'ns0:title' with the others to get the rest of the entry data

class YouTubeAPI(object):

  #def __init__(self, queryList): #Set up our search..could move to runQuery?
    #self.queryList = queryList
    #self.queryString = ""
    #for index in range(len(queryList)): #Figure out if we have more than one search term and make an OR operation
      #if index == len(queryList)-1:
        #self.queryString += str(queryList[index])
      #else:
        #self.queryString += str(queryList[index]) + "|" # '|' is the OR operator for more results
    #print "Ready to search YouTube with " + self.queryString
      
  def runQuery(self, searchTerm, numResults, start_index): #Client search youtube API
    if numResults > 50: #YouTube gets mad if you go over 50
      #print "Maximum results returned by single query is \"50\""
      #print "Changing value to \"50\""
      numResults = 50      
    try:    #Try to run query using YouTube API
      client = gdata.youtube.service.YouTubeService()
      query = gdata.youtube.service.YouTubeVideoQuery()
      query.vq = searchTerm #Our search terms
      query.max_results = str(numResults) #How many returned
      query.start_index = start_index # normally '1' This will need to be employed later to retrieve next 50 results
      query.racy = 'exclude' #include or exclude restricted content
      query.format = '5' #Specifies video format
      query.orderby = 'published' #relevance, viewCount, published, or rating
      query.location = '' #Setting this to a string returns results that only have GEO data
      self.feed = client.YouTubeQuery(query) #Run the damn query already!
      self.feedText = str(self.feed).decode('utf-8') #This may not be clean code or needed
    except:
      raise "Unexpected error: ", sys.exc_info()[0]
    return self.parseXML()
  def parseXML(self):
      # 3 XML handler functions
      self.dictList = [] #set up empty list for dictionaries to go into
      self.dict_ = {} #set up empty dictionary for entries to go into
      self.definition = '' #set up empty definition for tag data
      self.entryCount = 0 #set up counter
      def start_element(name, attrs): #Name is the part of the XML we want
          self.term = str(name) #Turn it into a string
      def char_data(data):    #The payload between the tags gets parsed here
        if data: # don't bother if there's no data
            self.definition = data.encode( "utf-8" )
            if self.term in self.dict_:
              self.dict_[self.term] = self.dict_[self.term] + self.definition
            else:
              self.dict_[self.term] = self.definition
      def end_element(name):
        if name == 'ns0:entry': #we only care if it gets to the end of the entry
            try:
                for link in self.feed.entry[self.entryCount].link: #use the gdata.youtube lib for this one good thing, to get the right link
                    self.link = link.href
                    break #The first link is the one for web sites so we stop
            except:
                raise "Unexpected error: ", sys.exc_info()[0] 
            self.term = 'ns0:link' #Create our own term for the link we want
            self.dict_[self.term] = self.link #Insert our own link definition from above
            soup = BeautifulSoup(self.dict_['ns0:content'])
            for link in soup.a:
              self.thumbnailURL = (link.get('src'))
            self.term = 'ns0:thumb'
            self.dict_[self.term] = str(self.thumbnailURL)
            URL = self.dict_['ns0:thumb']
            urlsegments = URL.rpartition('/')
            idsegments = urlsegments[0].rpartition('/vi/')
            self.term = 'ns0:video_id'
            self.dict_[self.term] = str(idsegments[2])
            self.dictList.append(self.dict_) #Add new API entry
            self.dict_ = {} #Clear the dictionary
            self.entryCount = self.entryCount + 1 #Update our position in the list
      p = xml.parsers.expat.ParserCreate('utf-8') #Create parser object
      p.StartElementHandler = start_element #Call start element handler
      p.CharacterDataHandler = char_data #Parse the data between tags
      p.EndElementHandler = end_element #Used to find the end of our entry
      p.Parse(self.feedText.encode( "utf-8" ), 1) #Call parse of the text returned from the API fee
      return self.dictList #For development purposes?
