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

from spi import *
from spi.binary import marshall, Ensemble
from spi.binary.bands import *

import datetime
import logging

#logging.basicConfig(level=logging.DEBUG)

info = ServiceInfo(originator='Global Radio', 
                   provider='Global Radio', 
                   created=datetime.datetime(2014, 04, 25, 0, 50, 31, 0))

# Ensemble
ensemble = Ensemble(0xe1, 0xc479)
ensemble.names.append(ShortName('London 1'))
ensemble.names.append(MediumName('London 1'))
ensemble.frequencies.append(BAND_12C)

# Capital London 
service = Service()
service.names.append(ShortName('Capital'))
service.names.append(MediumName('Capital'))
service.names.append(LongName('Capital London'))
service.descriptions.append(ShortDescription('The UK\'s No.1 Hit Music Station'))
service.media.append(Multimedia('http://owdo.thisisglobal.com/2.0/id/25/logo/32x32.png',
                                Multimedia.LOGO_COLOUR_SQUARE))
service.media.append(Multimedia('http://owdo.thisisglobal.com/2.0/id/25/logo/112x32.png',
                                Multimedia.LOGO_COLOUR_RECTANGLE))
service.media.append(Multimedia('http://owdo.thisisglobal.com/2.0/id/25/logo/128x128.png',
                                type=Multimedia.LOGO_UNRESTRICTED,
                                width=128, height=128,
                                content='image/png'))
service.media.append(Multimedia('http://owdo.thisisglobal.com/2.0/id/25/logo/320x240.png',
                                type=Multimedia.LOGO_UNRESTRICTED,
                                width=320, height=240,
                                content='image/png'))
service.media.append(Multimedia('http://owdo.thisisglobal.com/2.0/id/25/logo/800x600.png',
                                type=Multimedia.LOGO_UNRESTRICTED,
                                width=800, height=600,
                                content='image/png'))
service.media.append(Multimedia('http://owdo.thisisglobal.com/2.0/id/25/logo/1024x768.png',
                                type=Multimedia.LOGO_UNRESTRICTED,
                                width=1024, height=768,
                                content='image/png'))
service.genres.append(Genre('urn:tva:metadata:cs:ContentCS:2004:3.6.10'))
service.genres.append(Genre('urn:tva:metadata:cs:ContentCS:2004:3.6.8'))
service.genres.append(Genre('urn:tva:metadata:cs:ContentCS:2004:3.6.8.14'))
service.genres.append(Genre('urn:tva:metadata:cs:ContentCS:2004:3.1.4.12'))
service.keywords.extend(['London', 'music', 'pop', 'rock', 'dance', 'urban'])
service.links.append(Link('http://www.capitalfm.com/london', content='text/html'))
service.links.append(Link('sms:83958'))
service.bearers.append(DabBearer(0xe1, 0xc185, 0xc479, 0x0, content='audio/mpeg', offset=2000, cost=20)) 
service.bearers.append(IpBearer('http://media-ice.musicradio.com/Capital', content='audio/aacp', offset=4000, cost=40, bitrate=48))
service.bearers.append(IpBearer('http://media-ice.musicradio.com/CapitalMP3Low', content='audio/mpeg', offset=4000, cost=40, bitrate=48))
service.lookup = 'http://www.capitalfm.com/london'
service.geolocations.append(Country('GB'))
service.geolocations.append(Polygon.fromstring('51.524124 -2.709503 51.572803 -2.668304 51.616310 -2.572174 51.575363 -2.412872 51.504471 -2.379913 51.426613 -2.471924 51.400063 -2.460937 51.387211 -2.511749 51.328896 -2.708130 51.273087 -2.772675 51.238705 -2.938843 51.258476 -3.036346 51.376068 -3.026733 51.472401 -2.859879 51.524124 -2.709503'))
info.services.append(service)

# Capital Group
group = ServiceGroup('capital')
group.names.append(ShortName('Capital'))
group.names.append(MediumName('Capital FM'))
group.descriptions.append(ShortDescription('The UK\'s No.1 Hit Music Station'))
group.media.append(Multimedia('http://owdo.thisisglobal.com/2.0/id/25/logo/32x32.png',
                                Multimedia.LOGO_COLOUR_SQUARE))
group.media.append(Multimedia('http://owdo.thisisglobal.com/2.0/id/25/logo/112x32.png',
                                Multimedia.LOGO_COLOUR_RECTANGLE))
group.media.append(Multimedia('http://owdo.thisisglobal.com/2.0/id/25/logo/128x128.png',
                                type=Multimedia.LOGO_UNRESTRICTED,
                                width=128, height=128,
                                content='image/png'))
group.media.append(Multimedia('http://owdo.thisisglobal.com/2.0/id/25/logo/320x240.png',
                                type=Multimedia.LOGO_UNRESTRICTED,
                                width=320, height=240,
                                content='image/png'))
group.media.append(Multimedia('http://owdo.thisisglobal.com/2.0/id/25/logo/800x600.png',
                                type=Multimedia.LOGO_UNRESTRICTED,
                                width=800, height=600,
                                content='image/png'))
group.media.append(Multimedia('http://owdo.thisisglobal.com/2.0/id/25/logo/1024x768.png',
                                type=Multimedia.LOGO_UNRESTRICTED,
                                width=1024, height=768,
                                content='image/png'))
group.links.append(Link('http://en.wikipedia.org/wiki/Capital_(radio_network)"', content='text/html', description='Capital on Wikipedia'))

group.services.append(service)
info.groups.append(group)


print marshall(info, ensemble=ensemble)
