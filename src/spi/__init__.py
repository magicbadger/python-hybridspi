#===============================================================================
# Python Hybrid Radio SPI - API to support ETSI TS 102 818
# 
# Copyright (C) 2010 Global Radio
# Copyright (C) 2015 Ben Poor
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#===============================================================================


import datetime
import re
from dateutil.tz import tzlocal

MAX_SHORTCRID = 16777215
DEFAULT_LANGUAGE = "en"

class Text:
    """Abstract class for textual information"""
    
    def __init__(self, text, max_length, language = None):
        if not isinstance(text, str): raise ValueError('text must be of a basestring subtype, not %s: %s', type(text), text)
        if len(text) > max_length: raise ValueError('text length exceeds the maximum: %d>%d' % (len(text), max_length))
        self.max_length = max_length
        self.text = text
        self.language = language if language is not None else DEFAULT_LANGUAGE
        
    def __str__(self):
        return self.text

    def __repr__(self):
        return '<Text[%d]: %s>' % (self.max_length, self.text)
    
class LongDescription(Text):
    """Long descriptive text, with maximum length of 1800 characters"""
    
    max_length = 1800
    
    def __init__(self, text, language = None):
        Text.__init__(self, text, 1800, language)

class ShortDescription(Text):
    """Short descriptive text, with maximum length of 180 characters"""
    
    max_length = 180
    
    def __init__(self, text, language = None):
        Text.__init__(self, text, 180, language)
        
class LongName(Text):
    """Long name text, with maximum length of 128 characters"""
    
    max_length = 128
    
    def __init__(self, text, language = None):
        Text.__init__(self, text, 128, language)

class MediumName(Text):
    """Medium name text, with maximum length of 16 characters"""

    max_length = 16
    
    def __init__(self, text, language = None):
        Text.__init__(self, text, 16, language)
        
class ShortName(Text):
    """Short name text, with maximum length of 8 characters"""
    
    max_length = 8
    
    def __init__(self, text, language = None):
        Text.__init__(self, text, 8, language)    
        
def suggest_names(names):   
    """Returns a list of names best fitting to the lengths of the original
    strings passed in"""
      
    result = []
    for name in names:
        if len(name) > MediumName.max_length:
            result.append(MediumName(name[0:MediumName.max_length-1]))
            result.append(LongName(name))
        elif len(name) > ShortName.max_length:
            result.append(ShortName(name[0:ShortName.max_length-1]))
            result.append(MediumName(name))
            result.append(LongName(name))
        else:
            result.append(ShortName(name))
            result.append(MediumName(name))
            result.append(LongName(name))            
    return result
 
class Named:
    """
    Holds and returns names in a variety of lengths: Short, Medium, Long
    """
    
    def __init__(self):
        self.names = []
    
    def get_name(self, max_length=LongName.max_length):
        """
        Returns the first name set with a length at or below the max_length field, which 
        defaults to the MAX_LENGTH of a LongName field
        """
        for t in [LongName, MediumName, ShortName]:
            for name in [x for x in self.names if isinstance(x, t)]:
                if len(name.text) <= max_length: return name        

    def get_names(self, max_length=LongName.max_length):
        """
        Returns zero or more names with a length at or below the max_length field, which 
        defaults to the MAX_LENGTH of a LongName field
        """
        result = []
        for t in [LongName, MediumName, ShortName]:
            for name in [x for x in self.names if isinstance(x, t)]:
                if len(name.text) <= max_length: result.append(name) 
        return result

class Described:
    """
    Holds and returns descriptions in a variety of lengths
    """
    
    def __init__(self):
        self.descriptions = []

    def get_description(self, max_length=LongDescription.max_length):
        """returns the first description set with a length at or below the max_length field, which 
           defaults to the MAX_LENGTH of a LongDescription field"""
        for type in [LongDescription, ShortDescription]:
            for description in [x for x in self.media if isinstance(x, type)]:
                if len(description.text) <= max_length: return description        
     
class Geolocated:
    """
    An entity that can have geolocation information added to it
    """

    def __init__(self):
        self.geolocations = []
       
 
class Bearer(Geolocated):  
    """
    Service bearer, the details of which are contained within a URI, as per the BearerURI syntax
    defined in the Hybrid Radio Lookup specification, TS 103 270
    """

    cost = None
    offset = None

    def __init__(self, cost : int = None, offset : int = None):
        if cost is not None: self.cost = int(cost)
        if offset is not None: self.offset = offset

    def __str__(self):
        raise ValueError('__str__ function not defined in type: %s' % type(self))

class DigitalBearer(Bearer):
    """
    Digital bearer superclass
    """

    bitrate = None
    content = None

    def __init__(self, content : str, cost : int=None, offset : int=0, bitrate : int=None):
        Bearer.__init__(self, cost, offset)
        if bitrate is not None: self.bitrate = int(bitrate)
        self.content = content

    def __str__(self):
        raise ValueError('__str__ function not defined in type: %s' % type(self))        

class DabBearer(DigitalBearer):

    DAB = 'audio/mpeg'
    DAB_PLUS = 'audio/aacp'

    def __init__(self, ecc, eid, sid, scids=0, content=DAB_PLUS, xpad=None, cost=None, offset=None, bitrate=None):

        """
        DAB Service Bearer

        ::    
        dab:<gcc>.<eid>.<sid>.<scids>.<xpad> in hex
        :: 

        Where ``gcc`` is a combination of the first nibble of the SId and the ECC.

        For example:
        ::
            dab:ce1.ce15.c221.0.1
        :: 

        :param ecc: Extended Country Code
        :type ecc: int
        :param eid: Ensemble ID
        :type eid: int
        :param sid: Service ID 
        :type sid: int
        :param scids: Service Component ID within the Service 
        :type scids: int
        :param xpad: X-PAD application 
        :type xpad: int
        """
     
        DigitalBearer.__init__(self, cost=cost, offset=offset, bitrate=bitrate, content=content)
        self.ecc = ecc
        self.sid = sid
        self.eid = eid
        self.scids = scids
        self.xpad = xpad

        if not isinstance(ecc, int): raise ValueError("ECC must be an integer")
        if not isinstance(eid, int): raise ValueError("EId must be an integer")
        if not isinstance(sid, int): raise ValueError("SId must be an integer")
        if not isinstance(scids, int): raise ValueError("SCIdS must be an number")
        if xpad and not isinstance(xpad, int): raise ValueError("XPAD AppType must be an integer")
        
    @classmethod
    def fromstring(cls, string):
        """
        Parse a DAB Bearer URI from its string representation
        """        
        
        pattern = re.compile("^dab:([0-9a-f]{3})\.([0-9a-f]{4})\.([0-9a-f]{4,8})\.([0-9a-f]{1})[\.(.+?)]{0,1}$")
        matcher = pattern.search(string)
        if not matcher: raise ValueError('bearer %s does not match the pattern: %s' % (string, pattern.pattern))
        ecc = int(matcher.group(1)[1:], 16)
        eid = int(matcher.group(2), 16)
        sid = int(matcher.group(3), 16)
        scids = int(matcher.group(4), 16)
        xpad = None
        if len(matcher.groups()) > 4:
            xpad = int(matcher.group(5))
        return DabBearer(ecc, eid, sid, scids, xpad)
    
    def __str__(self):
        if self.sid>65535: # this is a long SId which contains both ECC (first two nibbles) and CC (third nibble)
            gcc = (self.sid >> 12 & 0xf00) + (self.sid >> 24)
            uri = 'dab:{gcc:03x}.{eid:04x}.{sid:08x}.{scids:01x}'.format(gcc=gcc, eid=self.eid, sid=self.sid, scids=self.scids)
        else: # this is a short SId which contains only the CC (first nibble)
            gcc = (self.sid >> 4 & 0xf00) + self.ecc
            uri = 'dab:{gcc:03x}.{eid:04x}.{sid:04x}.{scids:01x}'.format(gcc=gcc, eid=self.eid, sid=self.sid, scids=self.scids)
 
        if self.xpad is not None:
            uri += '.{xpad:04x}'.format(xpad=self.xpad)
        return uri

    def __repr__(self):
        return '<DabBearer: %s>' % str(self)

    def __eq__(self, other):
        return str(self) == str(other)
            
class HdBearer(DigitalBearer):

    def __init__(self, tx, cc, mId=None, cost=None, offset=None):

        """
        HD Service Bearer

        ::    
        hd:<tx>.<cc>.<mId> in hex
        :: 

        :param tx: Transmitter Identifier
        :type tx: int
        :param cc: Country code
        :type cc: int
        :param mId: Multocast programme service
        :type mId: int
        """
     
        HdBearer.__init__(self, cost=cost, offset=offset, bitrate=None, content=None)
        self.tx = tx
        self.cc = cc
        self.mId = mId
        
    def __str__(self):
        uri = 'hd:{tx:05x}.{cc:03x}.{sid:04x}.{scids:01x}'.format(gcc=(self.eid >> 4 & 0xf00) + self.ecc, eid=self.eid, sid=self.sid, scids=self.scids)
        if self.xpad is not None:
            uri += '.{xpad:04x}'.format(xpad=self.xpad)
        return uri

    def __repr__(self):
        return '<DabBearer: %s>' % str(self)        

    def __eq__(self, other):
        return str(self) == str(other)

class FmBearer(Bearer):

    def __init__(self, ecc, pi, frequency, cost=None, offset=None):
        """
        FM Service Bearer

        ::    
        fm:<gcc>.<pi>.<Frequency in 100Hz, zero padded to 5 chars>
        :: 

        For example:
        ::
            fm:ce1.c479.09580
        :: 

        :param ecc: Extended Country Code
        :type ecc: int
        :param pi: Programme Info code
        :type pi: int
        :param frequency: Service frequency (Hz)
        :type frequency: int
        """
     
        Bearer.__init__(self, cost, offset)
        self.ecc = ecc
        self.pi = pi
        self.frequency = frequency

        if not isinstance(ecc, int): raise ValueError("ECC must be an integer")
        if not isinstance(pi, int): raise ValueError("PI must be an integer")
        if not isinstance(frequency, int): raise ValueError("Frequency must be an integer")
        
    @classmethod
    def fromstring(cls, string):
        """
        Parse a FM Bearer URI from its string representation
        """        
        
        pattern = re.compile("fm:(.{3})\.(.{4})\.(.{5})")
        matcher = pattern.search(string)
        if not matcher: raise ValueError('bearer %s does not match the pattern: %s' % (string, pattern))
        ecc = int(matcher.group(1)[1:], 16)
        pi = int(matcher.group(2), 16)
        frequency = int(matcher.group(3)) * 10
        return FmBearer(ecc, pi, frequency)
    
    def __str__(self):
        uri = 'fm:{gcc:03x}.{pi:04x}.{frequency:05d}'.format(gcc=(self.pi >> 4 & 0xf00) + self.ecc, pi=self.pi, frequency=int(self.frequency/10))
        return uri
    
    def __repr__(self):
        return '<FmBearer: %s>' % str(self)
    
    def __eq__(self, other):
        return str(self) == str(other)

class IpBearer(DigitalBearer):

    def __init__(self, uri, content=None, cost=None, offset=None, bitrate=None):

        """
        IP Service Bearer

        :param uri: IP stream URI 
        :type uri: URI
        """
     
        DigitalBearer.__init__(self, content, cost=cost, offset=offset, bitrate=bitrate)
        self.uri = uri

    def __str__(self):
        return self.uri
    
    def __repr__(self):
        return '<IpBearer: %s>' % str(self)

    def __eq__(self, other):
        return str(self) == str(other)

class ProgrammeInfo:
    """The root of a PI document"""
    
    def __init__(self, schedules=[]):
        self.schedules = schedules
    
class Link:
    """
    This is used to link from a service, programme, programmeEvent or programmeGroup to an additional resource. 
    This may be additional content, data, or interaction related to the parent element.
    """    
        
    def __init__(self, uri, content=None, description=None, expiry=None, language=None):
        self.uri = uri
        self.content = content
        self.description = description
        self.expiry = expiry
        self.language = language
        
    def __str__(self):
        return self.uri
        
        
class Location:
    """
    This element specifies the times and bearers on which a programme or programme event is available, or the relative times and bearers on which a programme event is available in a linear schedule. The location element may appear zero or more times within a programme or programmeEvent element.
    """
    
    def __init__(self, times=None, bearers=None):
        self.times = times if times is not None else []
        self.bearers = [] if bearers is None else [] 
        
    def __str__(self):
        return '{times} times, {bearers} bearers'.format(times=len(self.times), bearers=len(self.bearers)) 
    
    def __repr__(self):
        return '<Location: %s>' % str(self)
        
        
class BaseTime:
    """Base for Absolute and Relative times"""
    
    def get_billed_time(self, base):
        raise ValueError('not implemented')
        
    def get_billed_duration(self):
        raise ValueError('not implemented')
        
    def get_actual_time(self, base):
        raise ValueError('not implemented')
        
    def get_actual_duration(self):
        raise ValueError('not implemented')
    
    
class RelativeTime(BaseTime):
    """
    Time for a :class:ProgrammeEvent relative to the start of the containing :class:Programme
    """
    
    def __init__(self, billed_offset, billed_duration, actual_offset=None, actual_duration=None):
        self.actual_offset = actual_offset
        self.actual_duration = actual_duration
        self.billed_offset = billed_offset
        self.billed_duration = billed_duration
    
    def get_billed_time(self, base):
        if self.billed_offset is None: return None
        return base + self.billed_offset
        
    def get_billed_duration(self):
        return self.billed_duration
        
    def get_actual_time(self, base):
        if self.actual_offset is None: return None
        return base + self.actual_offset
        
    def get_actual_duration(self):
        return self.actual_duration
    
    def __str__(self):
        return 'offset=%s, duration=%s' % (str(self.billed_offset), str(self.billed_duration))
    
    def __repr__(self):
        return '<RelativeTime: %s>' % str(self)

        
class Time(BaseTime):
    """Absolute time for a :class:ProgrammeEvent or :class:Programme"""
    
    def __init__(self, billed_time, billed_duration, actual_time=None, actual_duration=None):
        self.actual_time = actual_time
        self.actual_duration = actual_duration
        self.billed_time = billed_time
        self.billed_duration = billed_duration
    
    def get_billed_time(self, base=None):
        return self.billed_time
        
    def get_billed_duration(self):
        return self.billed_duration
        
    def get_actual_time(self, base=None):
        return self.actual_time
        
    def get_actual_duration(self):
        return self.actual_duration

    def __str__(self):
        return 'time=%s, duration=%s' % (str(self.billed_time), str(self.billed_duration))
    
    def __repr__(self):
        return '<Time: %s>' % str(self)

       
      
class Membership:
    """The member of a :class:Programme or :class:ProgrammeEvent to a group, references by a
    Short Crid
    
    :param shortcrid: Short Crid
    :type shortcrid: int
    :param crid: Full Crid
    :type crid: Crid
    :param index: Index within the group membership
    :type index: int    
    """
    
    def __init__(self, crid, shortcrid,index=None):
        self.crid = crid
        if type(shortcrid) != int: raise ValueError('shortcrid must be an integer')
        self.shortcrid = shortcrid
        self.index = index 
        
    def __str__(self):
        return str(self.shortcrid)
    
    def __repr__(self):
        return '<Membership: shortcrid=%d, crid=%s, index=%s>' % (self.shortcrid, self.crid, str(self.index))
    
class Multimedia:
    """Link to a multimedia element attached to a :class:Programme or :class:ProgrammeEvent
    
    :param url: URL to the multimedia resource
    :type url: str
    :param type: Type of Multimedia resource
    :type type: str
    :param content: MIME type of the multimedia resource
    :type content: str    
    :param height: height of the multimedia resource in pixels
    :type height: int      
    :param width: width of the multimedia resource in pixels
    :type width: int   
    """
    
    LOGO_UNRESTRICTED ="logo_unrestricted"    
    LOGO_COLOUR_SQUARE = "logo_colour_square"
    LOGO_COLOUR_RECTANGLE = "logo_colour_rectangle"
    
    def __init__(self, url, type=LOGO_UNRESTRICTED, content=None, height=None, width=None, language=None):
        self.url = url
        self.type = type
        self.content = content
        self.height = height
        self.width = width
        if type == Multimedia.LOGO_UNRESTRICTED and (not height or not width or not content):
            raise ValueError('an unrestricted logo must have height, width and content type defined') 
        self.language = language
        
class Programme(Named, Described):
    """Describes and locates a programme.
    
    :param crid: Full Crid
    :type crid: str  
    :param shortcrid: Short Crid
    :type shortcrid: int    
    :param onair: True to flag as a recommended programme
    :type onair: bool  
    :param version: Programme metadata version
    :type version: int
    """   
    
    def __init__(self, crid, shortcrid, recommendation=False, version=1):
        Named.__init__(self)
        Described.__init__(self)
        self.crid = crid
        self.shortcrid = int(shortcrid)
        self.version = version
        self.recommendation = recommendation
        self.locations = []
        self.media = []
        self.genres = []
        self.keywords = []
        self.memberships = []
        self.links = []
        self.events = []
        
    def get_bearers(self):
        """return a list of bearers collated from the locations of this programme"""

        bearers = []
        for location in self.locations:
            bearers.extend(location.bearers)
        result = [] # remove diplicates now
        for bearer in bearers:
            if bearer not in result: result.append(bearer)
        return result
            
    def get_times(self):
        """returns a list of (datetime, timedelta) tuples collated from the billed times of the locations
           of this programme"""
        times = []
        for location in self.locations:
            times.extend([(x.get_billed_time(), x.get_billed_duration()) for x in location.times])
        return times
        
    def __str__(self):
        return str(self.get_name())
    
    def __repr__(self):
        return '<Programme: %s>' % str(self)    
    
    
class ProgrammeEvent(Named, Described):
    """Describes and locates a programme event within a programme
    
    :param crid: Full Crid
    :type crid: str  
    :param shortcrid: Short Crid
    :type shortcrid: int    
    :param recommendation: True to flag as a recommended programme event
    :type recommendation: bool  
    :param version: Programme event metadata version
    :type version: int
    """       
    
    def __init__(self, crid, shortcrid, recommendation=False, version=1):
        Named.__init__(self)
        Described.__init__(self)
        self.crid = crid
        if type(shortcrid) != int: raise ValueError('shortcrid must be an integer')
        self.shortcrid = shortcrid
        self.recommendation = recommendation
        self.version = version
        self.locations = []
        self.media = []
        self.genres = []
        self.keywords = []
        self.memberships = []
        self.links = []
        
    def __str__(self):
        return str(self.get_name())
    
    def __repr__(self):
        return '<ProgrammeEvent: %s>' % str(self)
    
class Scope:
    """
    Contains the scope of the proposed schedule, in terms of time and bearers
    """

    def __init__(self, start=None, end=None, bearers=[]):
        """
        :param start: Scope start time, if not specified this is calculated from the programmes
        :type start: datetime
        :param end: Scope end time if not specified, this is calculated from the programmes
        :type end: datetime
        :param bearers: Bearers within the scope
        :type bearers: list
        """
        self.start = start
        self.end = end
        self.bearers = bearers

class Schedule:
    """
    Contains programmes within a given time period.
    """
    
    def __init__(self, scope=None, created=datetime.datetime.now(tzlocal()), version=1, originator=None):
        """x
        :param scope: Defined scope, otherwise proposed from the schedule
        :type scope: Scope
        :param created: Creation time of this element
        :type created: datetime
        :param version: Schedule version
        :type version: int
        :param originator: Originator of the schedule
        :type originator: string
        """
        if scope==None and type(scope) is not Scope: scope=Scope()
        if type(scope) is not Scope: raise ValueError("scope must be a Scope object")
        self.scope = scope
        self.created = created
        self.version = version
        self.originator = originator
        self.programmes = []

    def get_scope(self):
        if self.scope is not None: return self.scope

        scope_start = scope_end = None
        bearers = []

        for programme in self.programmes:
            for time in programme.get_times():
                start, duration = time
                end = start + duration
                if scope_start is None or start < scope_start: scope_start = start
                if scope_end is None or end > scope_end: scope_end = end
            for b in programme.get_bearers(): # remove duplicates
                if b not in bearers: bearers.append(b)

        return Scope(scope_start, scope_end, bearers)

class Lookup():
    """
    Contains RadioDNS Lookup parameters.
    """

    def __init__(self, fqdn, serviceIdentifier):
        """
        :param fqdn: RadioDNS Lookup FQDN
        :type fqdn: string
        :param serviceIdentifier: RadioDNS Lookup ServiceIdentifier
        :type serviceIdentifier: string
        """
        self.fqdn = fqdn
        self.serviceIdentifier = serviceIdentifier

    def __str__(self):
        return "%s/%s" % (self.fqdn, self.serviceIdentifier)

    def __repr__(self):
        return '<Lookup: %s>' % self

    @classmethod
    def fromstring(cls, string):
        from urllib.parse import urlparse
        p = urlparse(string)
        lookup = Lookup(p.netloc, p.path[1:]) # probably a bit hacky
        return lookup
        
class Service(Named, Described, Geolocated):
    
    def __init__(self, media=None, genres=None, links=None, keywords=None, lookup : Lookup=None, version=1):
        """
        Service definition
        
        :param media: Media definitions
        :type media: list of media objects
        :param genres: Service genres
        :type genres: list of genre URIs
        :param links: Associated content links
        :type links: list of URIs
        :param keywords: Service keywords
        :type keywords: list of keywords
        :param lookup: Hybrid radio lookup details 
        :type lookup: URI (http://<fqdn>/<serviceIdentifier>)
        :param version: Service definition version
        :type version: int
        """
        Named.__init__(self)
        Described.__init__(self)
        Geolocated.__init__(self)
        self.media = media if media else []
        self.genres = genres if genres else []
        self.links = links if links else []
        self.keywords = keywords if keywords else []
        self.lookup = lookup
        self.version = version
        self.bearers = []
                
    def __repr__(self):
        return '<Service: %s>' % str(self)
    
    def __str__(self):
        return str(self.get_name())
        
class ServiceInfo:
    
    def __init__(self, created=datetime.datetime.now(tzlocal()), version=1, originator=None, provider=None, language=DEFAULT_LANGUAGE):
        """
        Top-level Service Information document object

        :param created: Document creation datetime
        :type created: datetime
        :param version: Document version
        :type created: int
        :param originator: Document originator, i.e. the organisation that has prepared the document
        :type originator: string
        :param provider: Service Provider, i.e. the organisation providing the services in the document
        :type provider: string or :class:ServiceProvider
        """
        self.created = created
        self.version = version
        self.originator = originator
        self.provider = provider
        self.language = language
        self.services = []
        self.groups = []
         
class GroupInfo:

    def __init__(self):
        """
        Top-level Group Information document object
        """

        self.groupings = []    
    
class ProgrammeGroups:
    """Contains groups"""
    
    def __init__(self, created=datetime.datetime.now(tzlocal()), version=1, originator=None):
        self.created = created
        self.version = version
        self.originator = originator
        self.groups = []
    
class ProgrammeGroup(Named, Described):
    
    # type enum
    SERIES = "series"
    SHOW = "show"
    CONCEPT = "programConcept"
    MAGAZINE = "magazine"
    TOPIC = "topic"
    COMPILATION = "compilation"
    OTHER_COLLECTION = "otherCollection"
    OTHER_CHOICE = "otherChoice"
    
    def __init__(self, crid, shortcrid, type, numOfItems, version=1):
        """
        Programme group container

        :param crid: Full crid
        :type crid: crid uri
        :param shortcrid: Short crid
        :type shortcrid: int
        :param type: Grouping type
        :type type: Programme group type
        :param numOfItems: Number of items in the group
        :type numOfItems: int
        :param version: Programme group version
        :type version: int
        """
        Named.__init__(self)
        Described.__init__(self)
        self.crid = crid
        if not isinstance(shortcrid, int): raise ValueError('shortcrid must be an integer')
        self.shortcrid = shortcrid
        self.type = type
        self.numOfItem = numOfItems
        self.version = version
        self.media = []
        self.genres = []
        self.keywords = []
        self.memberships = []
        self.links = []

class ServiceProvider(Named, Described, Geolocated):

    def __init__(self, media=None, links=None, keywords=None):
        """
        Service Provider definition
        
        :param media: Media definitions
        :type media: list of media objects
        :param links: Associated content links
        :type links: list of URIs
        :param keywords: Service keywords
        :type keywords: list of keywords
        """
        Named.__init__(self)
        Described.__init__(self)
        Geolocated.__init__(self)
        self.media = media if media else []
        self.links = links if links else []
        self.keywords = keywords if keywords else []

class Country:

    def __init__(self, code):
        self.code = code

    def __str__(self):
        return self.code

    def __repr__(self):
        return '<Country: %s>' % str(self)

class Point:

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return "%s %s" % (self.latitude, self.longitude)

    def __repr__(self):
        return '<Point: %s>' % str(self)

class Polygon:

    def __init__(self, points=None):
        self.points = points if points else []

    @classmethod
    def fromstring(cls, string):
        points = []
        seq = string.split()
        if len(seq) % 2: raise ValueError('polygon string must have an even number of lat,lon')
        for i in range(0, len(seq), 2):
            p = Point(seq[i], seq[i+1])
            points.append(p)
        return Polygon(points)

    def __str__(self):
        return ' '.join([str(x) for x in self.points])

    def __repr__(self):
        return '<Polygon: %s>' % str(self)

class ServiceGroup(Named, Described, Geolocated):

    def __init__(self, id):
        Named.__init__(self)
        Described.__init__(self)
        Geolocated.__init__(self)
        self.id = id
        self.media = []
        self.genres = []
        self.links = []
        self.keywords = []
        self.services = []

class Genre:
    """
    Indicates the genre of a programme, group or service. The genre scheme is based on that used by the 
    TV-Anytime specification.
    
    :param href: Genre URI
    :type href: str  
    :param name: Descriptive name
    :type name: str
    """
    
    def __init__(self, href, name=None):
        self.href = href
        self.name = name     
        
    def __str__(self):
        return str(self.href)
    
    def __repr__(self):
        return '<Genre: %s>' % str(self)  
