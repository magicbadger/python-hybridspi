#===============================================================================
# Python Hybrid Radio SPI - API to support ETSI TS 102 818
# 
# Copyright (C) 2015, Ben Poor
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

from spi import *
import xml.dom.minidom
import isodate
from xml.dom import XML_NAMESPACE
from urlparse import urlparse
import logging

SCHEMA_NS = 'http://www.worlddab.org/schemas/spi/31'
SCHEMA_XSD = 'spi_31.xsd'
XSI_NS = 'http://www.w3.org/2001/XMLSchema-instance'

namespaces = { "spi" : SCHEMA_NS }

logger = logging.getLogger('spi.xml')

class MarshallListener:
    
    def on_element(self, doc, obj, element):
        pass
    
def marshall(obj, listener=MarshallListener(), indent=None, **kwargs):
    """
    Marshalls a :class:ProgrammeInfo, :class:GroupInfo or :class:ServiceInfo to its XML document
    """
    
    if isinstance(obj, ServiceInfo): return marshall_serviceinfo(obj, listener=listener, indent=indent, **kwargs)
    elif isinstance(obj, ProgrammeInfo): return marshall_programmeinfo(obj, listener=listener, indent=indent, **kwargs)
    elif isinstance(obj, GroupInfo): return marshall_groupinfo(obj, listener=listener, indent=indent, **kwargs)
    else: raise ValueError('Captain SPI says: neither a ServiceInfo, ProgrammeInfo not GroupInfo be')
    
def marshall_serviceinfo(info, listener=MarshallListener(), indent=None, **kwargs):
    """
    Encodes a ServiceInfo object into XML
    
    :info: object to encode
    :listener: Observer notified when an element is created
    :indent: Characters to use for XML indentation
    """
    

    doc = xml.dom.minidom.Document()
    
    # service info
    root = doc.createElement('serviceInformation')
    root.namespaceURI = SCHEMA_NS
    if info.version > 1: root.setAttribute('version', str(info.version))
    if info.created: root.setAttribute('creationTime', info.created.replace(microsecond=0).isoformat())
    if info.originator: root.setAttribute('originator', info.originator)
    if info.provider and isinstance(info.provider, basestring): root.setAttribute('serviceProvider', info.provider)   
    
    # fudge the namespaces in there
    root.setAttribute('xmlns', SCHEMA_NS)
    root.setAttribute('xmlns:xsi', XSI_NS)
    root.setAttribute('xsi:schemaLocation', '%s %s' % (SCHEMA_NS, SCHEMA_XSD))
    root.setAttribute('xml:lang', 'en')

    # services
    services_element = doc.createElement('services')
        
    # service provider
    if info.provider and isinstance(info.provider, ServiceProvider):
        provider = info.provider
        provider_element = doc.createElement('serviceProvider') 
        # names
        for name in provider.names:
            provider_element.appendChild(build_name(doc, name, listener))
        # descriptions
        for description in provider.descriptions:
            service_element.appendChild(build_description(doc, description, listener))
        # media
        for media in provider.media:
            provider_element.appendChild(build_mediagroup(doc, media, listener)) 
        # links
        for link in provider.links:
            provider_element.appendChild(build_link(doc, link, listener))                    
        # keywords
        if len(provider.keywords) > 0:
            keywords_element = doc.createElement('keywords')
            provider_element.appendChild(keywords_element)
            keywords_element.appendChild(doc.createCDATASection(', '.join(provider.keywords)))
        
        services_element.appendChild(provider_element)
         
    # service
    for service in info.services:
        service_element = doc.createElement('service')
        if service.version > 1: service_element.setAttribute('version', str(service.version))
        # names
        for name in service.names:
            service_element.appendChild(build_name(doc, name, listener))
        # descriptions
        for description in service.descriptions:
            service_element.appendChild(build_description(doc, description, listener))
        # media
        for media in service.media:
            service_element.appendChild(build_mediagroup(doc, media, listener)) 
        # genre
        for genre in service.genres:
            service_element.appendChild(build_genre(doc, genre, listener))    
        # links
        for link in service.links:
            service_element.appendChild(build_link(doc, link, listener))                    
        # keywords
        if len(service.keywords) > 0:
            keywords_element = doc.createElement('keywords')
            keywords_element.appendChild(doc.createCDATASection(', '.join(service.keywords)))
            listener.on_element(doc, service.keywords, keywords_element)
            service_element.appendChild(keywords_element)
        # bearers
        for bearer in service.bearers:
            service_element.appendChild(build_bearer(doc, bearer, listener))
        # lookup
        if service.lookup:
            from urlparse import urlparse
            url = urlparse(service.lookup)
            lookup_element = doc.createElement('radiodns')
            lookup_element.setAttribute('host', url.netloc)
            lookup_element.setAttribute('serviceIdentifier', url.path[1:])
            listener.on_element(doc, service.lookup, lookup_element)
            service_element.appendChild(lookup_element)
        # geolocation
        if len(service.geolocations) > 0:
            service_element.appendChild(build_geolocation(doc, service.geolocations, listener))            
            
        listener.on_element(doc, service, service_element)
        services_element.appendChild(service_element)
            
    listener.on_element(doc, info.services, services_element)
    root.appendChild(services_element)
        
    listener.on_element(doc, info, root)
    doc.appendChild(root)
        
    if indent:
        return doc.toprettyxml(indent=indent, encoding='UTF-8')
    else:
        return doc.toxml('UTF-8')

def marshall_programmeinfo(info, listener=MarshallListener(), indent=None):
    """
    Encodes a ProgrammeInfo object into XML
    
    :info: object to encode
    :listener: Observer notified when an element is created
    :indent: Characters to use for XML indentation
    """
    
    doc = xml.dom.minidom.Document()
    
    # epg
    epg_element = doc.createElement('epg')
    doc.appendChild(epg_element)
    
    # fudge the namespaces in there
    epg_element.setAttribute('xmlns', SCHEMA_NS)
    epg_element.setAttribute('xmlns:xsi', XSI_NS)
    epg_element.setAttribute('xsi:schemaLocation', '%s %s' % (SCHEMA_NS, SCHEMA_XSD))
    epg_element.setAttribute('xml:lang', 'en')
    
    # schedule
    for schedule in info.schedules:
        schedule_element = doc.createElement('schedule')
        epg_element.appendChild(schedule_element)
        if schedule.version > 1: schedule_element.setAttribute('version', str(schedule.version))
        schedule.created = schedule.created.replace(microsecond=0)
        schedule_element.setAttribute('creationTime', schedule.created.isoformat())
        if schedule.originator is not None:
            schedule_element.setAttribute('originator', schedule.originator)
            
        # scope
        scope_element = doc.createElement('scope')
        scope_element.setAttribute('startTime', schedule.start.isoformat())
        scope_element.setAttribute('stopTime', schedule.end.isoformat())
        listener.on_element(doc, schedule, scope_element)
        schedule_element.appendChild(scope_element)
        
        # programmes
        for programme in schedule.programmes:
            programme_element = doc.createElement('programme')
            programme_element.setAttribute('shortId', str(programme.shortcrid))
            programme_element.setAttribute('id', str(programme.crid))
            if programme.version > 1:
                programme_element.setAttribute('version', str(programme.version))
            if programme.recommendation:
                programme_element.setAttribute('recommendation', 'yes')
            # names
            for name in programme.names:
                child = build_name(doc, name, listener)
                programme_element.appendChild(child)
            # locations
            for location in programme.locations:
                child = build_location(doc, location, listener)
                programme_element.appendChild(child)    
            # descriptions
            for description in programme.descriptions:
                child = build_description(doc, description, listener)
                programme_element.appendChild(child)
            # media
            for media in programme.media:
                child = build_mediagroup(doc, media, listener)
                programme_element.appendChild(child)     
            # genre
            for genre in programme.genres:
                child = build_genre(doc, genre, listener)
                programme_element.appendChild(child)    
            # membership
            for membership in programme.memberships:
                child = build_membership(doc, membership, listener)
                programme_element.appendChild(child)    
            # link
            for link in programme.links:
                child = build_link(doc, link, listener)
                programme_element.appendChild(child)      
            # events
            for event in programme.events:
                child = build_programme_event(doc, event, listener)
                programme_element.appendChild(child) 
                
            schedule_element.appendChild(programme_element)
                
            listener.on_element(doc, programme, programme_element)
            
    listener.on_element(doc, info, epg_element)
        
    if indent:
        return doc.toprettyxml(indent=indent, encoding='UTF-8')
    else:
        return doc.toxml('UTF-8')
    
def marshall_groupinfo(info, listener=MarshallListener(), indent=None):
    """
    Encodes a GroupInfo object into XML
    
    :info: GroupInfo object to serialise 
    :listener: Observer notified when an element is created
    :indent: Characters to use for XML indentation
    """
    
    doc = xml.dom.minidom.Document()
    
    # epg
    epg_element = doc.createElement('epg')
    doc.appendChild(epg_element)
    
    # fudge the namespaces in there
    epg_element.setAttribute('xmlns', SCHEMA_NS)
    epg_element.setAttribute('xmlns:xsi', XSI_NS)
    epg_element.setAttribute('xsi:schemaLocation', '%s %s' % (SCHEMA_NS, SCHEMA_XSD))
    epg_element.setAttribute('xml:lang', 'en')
    
    # groupings
    for grouping in info.groupings:
        grouping_element = doc.createElement('programmeGroups')
        epg_element.appendChild(grouping_element)
        if grouping.version > 1: grouping_element.setAttribute('version', str(grouping.version))
        created = grouping.created.replace(microsecond=0)
        grouping_element.setAttribute('creationTime', created.isoformat())
        if grouping.originator is not None:
            grouping_element.setAttribute('originator', grouping.originator)
            
        # groups
        for group in grouping.groups: 
            group_element = doc.createElement('programmeGroup')
            group_element.setAttribute('id', str(group.crid))
            group_element.setAttribute('shortId', str(group.shortcrid))
            if group.version > 1:
                group_element.setAttribute('version', str(group.version))
            if group.type is not None:
                group_element.setAttribute('type', str(group.type))
            # names
            for name in group.names:
                child = build_name(doc, name, listener)
                group_element.appendChild(child)
            for description in group.descriptions:
                child = build_description(doc, description, listener)
                group_element.appendChild(child)
            # media
            for media in group.media:
                child = build_mediagroup(doc, media, listener)
                group_element.appendChild(child)     
            # genre
            for genre in group.genres:
                child = build_genre(doc, genre, listener)
                group_element.appendChild(child)    
            # membership
            for membership in group.memberships:
                child = build_membership(doc, membership, listener)
                group_element.appendChild(child)    
            # link
            for link in group.links:
                child = build_link(doc, link, listener)
                group_element.appendChild(child)      
                
            grouping_element.appendChild(group_element)
                
            listener.on_element(doc, group, group_element)
            
        listener.on_element(doc, grouping, grouping_element)
    
    listener.on_element(doc, info, epg_element)
        
    if indent:
        return doc.toprettyxml(indent=indent, encoding='UTF-8')
    else:
        return doc.toxml('UTF-8')
 


def build_name(doc, name, listener):
    name_element = None
    if isinstance(name, ShortName):
        name_element = doc.createElement('shortName')
    elif isinstance(name, MediumName):
        name_element = doc.createElement('mediumName')
    elif isinstance(name, LongName):
        name_element = doc.createElement('longName')
    name_element.appendChild(doc.createTextNode(name.text))
    listener.on_element(doc, name, name_element)
    return name_element

def build_bearer(doc, bearer, listener):
    bearer_element = doc.createElement('bearer')
    bearer_element.setAttribute('id', str(bearer))
    if bearer.cost:
        bearer_element.setAttribute('cost', str(bearer.cost))
    if bearer.offset:
        bearer_element.setAttribute('offset', str(bearer.offset))
    if isinstance(bearer, DigitalBearer):
        if bearer.content:
            bearer_element.setAttribute('mimeValue', bearer.content)
        if bearer.bitrate:
            bearer_element.setAttribute('bitrate', str(bearer.bitrate))
    listener.on_element(doc, bearer, bearer_element)
    return bearer_element

def build_geolocation(doc, geolocations, listener):
    geo_element = doc.createElement('geolocation')
    for i in geolocations:
        if isinstance(i, Country):
            country_element = doc.createElement('country')
            country_element.appendChild(doc.createTextNode(i.code))
            listener.on_element(doc, i, country_element) 
            geo_element.appendChild(country_element)
        elif isinstance(i, Point):
            country_element = doc.createElement('point')
            country_element.appendChild(doc.createTextNode(i))
            listener.on_element(doc, i, country_element) 
            geo_element.appendChild(country_element)
        elif isinstance(i, Polygon):
            country_element = doc.createElement('polygon')
            country_element.appendChild(doc.createTextNode(' '.join([str(x) for x in i.points])))
            listener.on_element(doc, i, country_element) 
            geo_element.appendChild(country_element)
    listener.on_element(doc, geolocations, geo_element)
    return geo_element 
    
def build_location(doc, location, listener):
    location_element = doc.createElement('location')
    for time in location.times:
        if isinstance(time, Time):
            time_element = doc.createElement('time')
            location_element.appendChild(time_element)
            time_element.setAttribute('time', time.billed_time.isoformat())
            time_element.setAttribute('duration', get_iso_period(time.billed_duration))
            if time.actual_time:
                time_element.setAttribute('actualTime', time.actual_time.isoformat())
            if time.actual_duration:
                time_element.setAttribute('actualDuration', get_iso_period(time.actual_duration)) 
            listener.on_element(doc, time, time_element)
        elif isinstance(time, RelativeTime):
            time_element = doc.createElement('relativeTime')
            location_element.appendChild(time_element)
            time_element.setAttribute('time', get_iso_period(time.billed_offset))
            time_element.setAttribute('duration', get_iso_period(time.billed_duration)) 
            if time.actual_offset:
                time_element.setAttribute('actualTime', get_iso_period(time.actual_offset))
            if time.actual_duration:
                time_element.setAttribute('actualDuration', get_iso_period(time.actual_duration)) 
            listener.on_element(doc, time, time_element)
    for bearer in location.bearers:
        bearer_element = build_bearer(doc, bearer, listener) 
        location_element.appendChild(bearer_element)
    listener.on_element(doc, location, location_element)
    return location_element  
    
def build_description(doc, description, listener):
    mediagroup_element = doc.createElement('mediaDescription')
    if isinstance(description, ShortDescription):
        media_element = doc.createElement('shortDescription')
        mediagroup_element.appendChild(media_element)
        listener.on_element(doc, description, media_element)
        media_element.appendChild(doc.createCDATASection(description.text))
    elif isinstance(description, LongDescription):
        media_element = doc.createElement('longDescription')
        mediagroup_element.appendChild(media_element)
        listener.on_element(doc, description, media_element)
        media_element.appendChild(doc.createCDATASection(description.text))    
    listener.on_element(doc, description, mediagroup_element)
    return mediagroup_element

def build_mediagroup(doc, media, listener):
    mediagroup_element = doc.createElement('mediaDescription')
    media_element = doc.createElement('multimedia')
    mediagroup_element.appendChild(media_element)
    media_element.setAttribute('url', media.url)
    media_element.setAttribute('type', media.type)
    if media.type == Multimedia.LOGO_UNRESTRICTED:
        media_element.setAttribute('mimeValue', media.content)
        media_element.setAttribute('height', str(media.height))
        media_element.setAttribute('width', str(media.width))
    listener.on_element(doc, media, media_element)
    listener.on_element(doc, media, mediagroup_element)
    return mediagroup_element
    
def build_genre(doc, genre, listener):
    genre_element = doc.createElement('genre')
    genre_element.setAttribute('href', genre)
    listener.on_element(doc, genre, genre_element)
    return genre_element    
    
def build_membership(doc, membership, listener):
    membership_element = doc.createElement('memberOf')
    membership_element.setAttribute('shortId', str(membership.shortcrid))
    membership_element.setAttribute('crid', str(membership.crid))
    if membership.index is not None: 
        membership_element.setAttribute('index', str(membership.index))
    listener.on_element(doc, membership, membership_element)
    return membership_element  
    
def build_link(doc, link, listener):
    link_element = doc.createElement('link')
    link_element.setAttribute('uri', link.uri)
    if link.description is not None:
        link_element.setAttribute('description', link.description)
    if link.content is not None:
        link_element.setAttribute('mimeValue', link.content)
    if link.expiry is not None:
        link_element.setAttribute('expiryTime', link.expiry.isoformat())
    listener.on_element(doc, link, link_element)
    return link_element   

def build_programme_event(doc, event, listener):
    event_element = doc.createElement('programmeEvent')
    event_element.setAttribute('shortId', str(event.shortcrid))
    event_element.setAttribute('id', str(event.crid))
    if event.version > 1:
        event_element.setAttribute('version', str(event.version))
    if event.recommendation is not False:
        event_element.setAttribute('recommendation', 'yes')

     # names
    for name in event.names:
        event_element.appendChild(build_name(doc, name, listener))
    # locations
    for location in event.locations:
        event_element.appendChild(build_location(doc, location, listener))    
    # media
    for media in event.media:
        event_element.appendChild(build_mediagroup(doc, media, listener))       
    # genre
    for genre in event.genres:
        event_element.appendChild(build_genre(doc, genre, listener)) 
    # membership
    for membership in event.memberships:
        event_element.appendChild(build_membership(doc, membership, listener))  
    # link
    for link in event.links:
        event_element.appendChild(build_link(doc, link, listener))   
             
    return event_element
    
def get_iso_period(duration):
    if isinstance(duration, int): duration = datetime.timedelta(seconds=duration)
    hours = (duration.days * 24) + duration.seconds / (60 * 60)
    minutes = (duration.seconds - hours * 60 * 60) / 60
    seconds = (duration.seconds - hours * 60 * 60 - minutes * 60)
    result = 'PT'
    if hours > 0: result += '%dH' % hours
    if minutes > 0: result += '%dM' % minutes
    if seconds > 0: result += '%dS' % seconds
    if hours == 0 and minutes == 0 and seconds == 0: result += '0S'
    return result

def get_schedule_filename(date, id):
    return '%s_%02x_%04x_%04x_%x_PI.xml' % (date.strftime('%Y%m%d'), id.ecc, id.eid, id.sid, id.scids)

def parse_serviceinfo(root):
    logger.debug('parsing service information')
    info = ServiceInfo()
    if root.attrib.has_key('creationTime'): info.created = isodate.parse_datetime(root.attrib['creationTime'])
    if root.attrib.has_key('version'): info.version = int(root.attrib['version'])
    if root.attrib.has_key('originator'): info.originator = root.attrib['originator']
    if root.attrib.has_key('serviceProvider'): info.provider = root.attrib['serviceProvider']
    if not root.attrib.has_key('{%s}lang' % XML_NAMESPACE): raise Exception('no xml:lang attribute declaration')
   
    # only one <services> element is supported for now 
    for service_element in root.find("spi:services", namespaces).findall("spi:service", namespaces):
        info.services.append(parse_service(service_element))
    
    return info

def parse_time(timeElement):
    if timeElement.tag == '{%s}time' % SCHEMA_NS:
        time = Time(isodate.parse_datetime(timeElement.attrib['time']),
                    isodate.parse_duration(timeElement.attrib['duration']),
                    isodate.parse_datetime(timeElement.attrib.get('actualTime')) if timeElement.attrib.has_key('actualTime') else None,
                    isodate.parse_duration(timeElement.attrib.get('actualDuration')) if timeElement.attrib.has_key('actualDuration') else None)
        return time
    if timeElement.tag == '{%s}relativeTime' % SCHEMA_NS:
        time = RelativeTime(isodate.parse_duration(timeElement.attrib['time']),
                    isodate.parse_duration(timeElement.attrib['duration']),
                    isodate.parse_duration(timeElement.attrib.get('actualTime')) if timeElement.attrib.has_key('actualTime') else None,
                    isodate.parse_duration(timeElement.attrib.get('actualDuration')) if timeElement.attrib.has_key('actualDuration') else None)
        return time
    else:
        raise ValueError('unknown time element: %s' % timeElement)

def parse_bearer(bearer_element):
    uri = bearer_element.attrib['id']
    if uri.startswith('dab'):
        bearer = DabBearer.fromstring(uri)
    elif uri.startswith('fm'):
        bearer = FmBearer.fromstring(uri) 
    elif uri.startswith('http'):
        bearer = IpBearer(uri)
    else:
        raise ValueError('bearer %s not recognised' % uri)

    if bearer_element.attrib.has_key('cost'):
        bearer.cost = int(bearer_element.attrib['cost'])
    if bearer_element.attrib.has_key('offset'):
        bearer.offset = int(bearer_element.attrib['offset'])
    if bearer_element.attrib.has_key('bitrate'):
        bearer.bitrate = int(bearer_element.attrib['bitrate'])
    if bearer_element.attrib.has_key('mimeValue'):
        bearer.content = bearer_element.attrib['mimeValue'] 

    return bearer
        
def parse_location(locationElement):
    location = Location()
    for timeElement in locationElement.findall('spi:time', namespaces): location.times.append(parse_time(timeElement))
    for timeElement in locationElement.findall('spi:relativeTime', namespaces): location.times.append(parse_time(timeElement))
    for bearerElement in locationElement.findall('spi:bearer', namespaces): location.bearers.append(parse_bearer(bearerElement))
    return location 

def parse_programme_event(programmeEventElement):
    event = ProgrammeEvent(programmeEventElement.attrib['shortId'])
    if programmeEventElement.attrib.has_key('id'): event.crid = programmeEventElement.attrib['id']
    if programmeEventElement.attrib.has_key('version'): event.version = int(programmeEventElement.attrib['version'])
    if programmeEventElement.attrib.has_key('recommendation'): event.recommendation = bool(programmeEventElement.attrib['recommendation'])

    for nameElement in programmeEventElement.findall("spi:shortName", namespaces): event.names.append(parse_name(nameElement))
    for nameElement in programmeEventElement.findall("spi:mediumName", namespaces): event.names.append(parse_name(nameElement))
    for nameElement in programmeEventElement.findall("spi:longName", namespaces): event.names.append(parse_name(nameElement))

    # media
    for media_element in programmeEventElement.findall("spi:mediaDescription", namespaces):
        for child in media_element.findall("spi:multimedia", namespaces):
            event.media.append(parse_multimedia(child))
        for child in media_element.findall("spi:shortDescription", namespaces):
            event.descriptions.append(parse_description(child))
        for child in media_element.findall("spi:longDescription", namespaces):
            event.descriptions.append(parse_description(child))

    for locationElement in programmeEventElement.findall("spi:location", namespaces): event.locations.append(parse_location(locationElement))
    for genreElement in programmeEventElement.findall("spi:genre", namespaces): event.genres.append(parse_genre(genreElement))
    for linkElement in programmeEventElement.findall("spi:link", namespaces): event.links.append(parse_link(linkElement))
    for keywordsElement in programmeEventElement.findall("spi:keywords", namespaces): event.keywords.extend(parse_keywords(keywordsElement))    
    
    return event

def parse_programme(programmeElement):
    programme = Programme(programmeElement.attrib['id'], programmeElement.attrib['shortId'])
    if programmeElement.attrib.has_key('version'): programme.version = int(programmeElement.attrib['version'])
    if programmeElement.attrib.has_key('recommendation'): programme.recommendation = bool(programmeElement.attrib['recommendation'])
    if programmeElement.attrib.has_key('broadcast'): programme.onair = True if programmeElement.attrib['broadcast'] == 'on-air' else False
    if programmeElement.attrib.has_key('bitrate'): programme.bitrate = int(programmeElement.attrib['bitrate'])

    for nameElement in programmeElement.findall("spi:shortName", namespaces): programme.names.append(parse_name(nameElement))
    for nameElement in programmeElement.findall("spi:mediumName", namespaces): programme.names.append(parse_name(nameElement))
    for nameElement in programmeElement.findall("spi:longName", namespaces): programme.names.append(parse_name(nameElement))

    # media
    for media_element in programmeElement.findall("spi:mediaDescription", namespaces):
        for child in media_element.findall("spi:multimedia", namespaces):
            programme.media.append(parse_multimedia(child))
        for child in media_element.findall("spi:shortDescription", namespaces):
            programme.descriptions.append(parse_description(child))
        for child in media_element.findall("spi:longDescription", namespaces):
            programme.descriptions.append(parse_description(child))

    for locationElement in programmeElement.findall("spi:location", namespaces): programme.locations.append(parse_location(locationElement))
    for genreElement in programmeElement.findall("spi:genre", namespaces): programme.genres.append(parse_genre(genreElement))
    for linkElement in programmeElement.findall("spi:link", namespaces): programme.links.append(parse_link(linkElement))
    for keywordsElement in programmeElement.findall("spi:keywords", namespaces): programme.keywords.extend(parse_keywords(keywordsElement))    
    
    for programmeEventElement in programmeElement.findall("spi:programmeEvent", namespaces): programme.events.append(parse_programme_event(programmeEventElement))
    
    return programme

def parse_schedule(scheduleElement):
    schedule = Schedule()
    if scheduleElement.attrib.has_key('creationTime'): schedule.created = isodate.parse_datetime(scheduleElement.attrib['creationTime'])
    if scheduleElement.attrib.has_key('version'): schedule.version = int(scheduleElement.attrib['version'])
    if scheduleElement.attrib.has_key('originator'): schedule.originator = scheduleElement.attrib['originator']
    
    for programmeElement in scheduleElement.findall('spi:programme', namespaces):
        schedule.programmes.append(parse_programme(programmeElement))
    return schedule

def parse_programmeinfo(root):
    logger.debug('parsing programme info from root: %s', root)
    schedules = []
    for schedule_element in root.findall('spi:schedule', namespaces):
        schedule = parse_schedule(schedule_element)
        schedules.append(schedule)
    info = ProgrammeInfo(schedules=schedules)
    return info

def parse_name(nameElement):
    if nameElement.tag == '{%s}shortName' % SCHEMA_NS:
        return ShortName(nameElement.text)
    elif nameElement.tag == '{%s}mediumName' % SCHEMA_NS:
        return MediumName(nameElement.text)
    elif nameElement.tag == '{%s}longName' % SCHEMA_NS:
        return LongName(nameElement.text)
    else:
        raise ValueError('unknown name element: %s' % nameElement)
    
def parse_description(descriptionElement):
    if descriptionElement.tag == '{%s}shortDescription' % SCHEMA_NS:
        return ShortDescription(descriptionElement.text)
    elif descriptionElement.tag == '{%s}longDescription' % SCHEMA_NS:
        return LongDescription(descriptionElement.text)   
    else:
        raise ValueError('unknown description element: %s' % descriptionElement)
    
def parse_multimedia(mediaElement):
    type = None
    mime = None
    width = None
    height = None
    if mediaElement.attrib.has_key('type'):
        type_str = mediaElement.attrib['type']
        if type_str == 'logo_colour_square': type = Multimedia.LOGO_COLOUR_SQUARE
        if type_str == 'logo_colour_rectangle': type = Multimedia.LOGO_COLOUR_RECTANGLE
        if type_str == 'logo_unrestricted': 
            type = Multimedia.LOGO_UNRESTRICTED
            if not mediaElement.attrib.has_key('mimeValue') or not mediaElement.attrib.has_key('width') or not mediaElement.attrib.has_key('height'):
                raise ValueError('must specify mimeValue, width and height for unrestricted logo: %s', mediaElement)
    if mediaElement.attrib.has_key('mimeValue'): mime = mediaElement.attrib['mimeValue']
    if mediaElement.attrib.has_key('width'): width = int(mediaElement.attrib['width'])
    if mediaElement.attrib.has_key('height'): height = int(mediaElement.attrib['height'])
        
    multimedia = Multimedia(mediaElement.attrib['url'], type=type, content=mime, height=height, width=width)
    return multimedia      
    
def parse_genre(genreElement):
    genre = Genre(genreElement.attrib['href'])
    genre.name = genreElement.text
    return genre  

def parse_link(linkElement):
    link = Link(linkElement.attrib['uri'])
    if linkElement.attrib.has_key('description'):
        link.description = linkElement.attrib['description']
    if linkElement.attrib.has_key('mimeValue'):
        link.content = linkElement.attrib['mimeValue']    
    if linkElement.attrib.has_key('expiryTime'):
        link.expiry = isodate.parse_datetime(linkElement.attrib['expiryTime']) 
    return link
        
def parse_keywords(keywordsElement):
    return map(lambda x: x.strip(), keywordsElement.text.split(','))
    
def parse_service(service_element):
    service = Service()
    
    # attributes
    if service_element.attrib.has_key('version'): service.version = int(service_element.attrib['version'])
    
    # names
    for child in service_element.findall("spi:shortName", namespaces): 
        service.names.append(parse_name(child))
    for child in service_element.findall("spi:mediumName", namespaces): 
        service.names.append(parse_name(child))
    for child in service_element.findall("spi:longName", namespaces): 
        service.names.append(parse_name(child))

    # bearers
    for child in service_element.findall("spi:bearer", namespaces):
        service.bearers.append(parse_bearer(child))

    # media
    for media_element in service_element.findall("spi:mediaDescription", namespaces): 
        for child in media_element.findall("spi:multimedia", namespaces):
            service.media.append(parse_multimedia(child))
        for child in media_element.findall("spi:shortDescription", namespaces):
            service.descriptions.append(parse_description(child))
        for child in media_element.findall("spi:longDescription", namespaces):
            service.descriptions.append(parse_description(child))

    # genres
    for child in service_element.findall("spi:genre", namespaces): 
        service.genres.append(parse_genre(child))

    # links
    for child in service_element.findall("spi:link", namespaces): 
        service.links.append(parse_link(child))

    # keywords
    for child in service_element.findall("spi:keywords", namespaces): 
        service.keywords.extend(parse_keywords(child))

    # lookup
    for child in service_element.findall("spi:radiodns", namespaces):
        service.lookup = 'http://%s/%s' % (child.attrib['fqdn'], child.attrib['serviceIdentifier'])
    
    return service

def parse_ensemble(ensembleElement):
    ensemble = Ensemble(ContentId.fromstring(ensembleElement.attrib['id']))
    for nameElement in ensembleElement.findall("spi:shortName", namespaces): ensemble.names.append(parse_name(nameElement))
    for nameElement in ensembleElement.findall("spi:mediumName", namespaces): ensemble.names.append(parse_name(nameElement))
    for nameElement in ensembleElement.findall("spi:longName", namespaces): ensemble.names.append(parse_name(nameElement))
    
    for frequencyElement in ensembleElement.findall("spi:frequency", namespaces):
        ensemble.frequencies.append(int(frequencyElement.attrib['kHz']))
        
    for service_element in ensembleElement.findall("spi:service", namespaces):
        ensemble.services.append(parse_service(service_element))
    return ensemble

def unmarshall(i):
    """Unmarshalls a PI or SI XML file to its respective :class:Epg or :class:ServiceInfo object
    
    :param i: String or File object to read XML from
    :type i: str, file
    """
    
    # read data
    import StringIO
    d = i if isinstance(i, file) else StringIO.StringIO(i)
    from xml.etree.ElementTree import parse 
    logger.debug('parsing XML data from: %s', d)
    doc = parse(d)
    root = doc.getroot()
    logger.debug('got root element: %s', root)
    
    if root.tag == '{%s}serviceInformation' % SCHEMA_NS:
        return parse_serviceinfo(root)
    elif root.tag == '{%s}epg' % SCHEMA_NS:
        if len(root.findall("spi:schedule", namespaces)):
            return parse_programmeinfo(root)
        if len(root.findall("spi:programmeGroups", namespaces)):
            return parse_groupinfo(root)
        else:
            raise Exception('epg element does not contain either schedules or programme groups')
    else:
        raise Exception('Arrgh! this be neither serviceInformation nor epg - to Davy Jones\' locker with ye!')   
    
