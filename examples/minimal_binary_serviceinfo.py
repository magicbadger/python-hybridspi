#===============================================================================
# Python Binary Encoding for Hybrid Radio SPI - API to support ETSI TS 102 370
# 
# Copyright (C) 2012, Global Radio
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
from spi.binary import Ensemble, marshall
from spi.binary.bands import BAND_5A

info = ServiceInfo()

# Service
service = Service()
service.bearers.append(DabBearer(0xe1, 0xcfff, 0xc0fe))
service.names.append(ShortName('Capital'))
service.names.append(MediumName('Capital London'))
service.media.append(Multimedia('capital_32x32.png', Multimedia.LOGO_COLOUR_SQUARE))
service.media.append(Multimedia('capital_112x32.png', Multimedia.LOGO_COLOUR_RECTANGLE))
service.media.append(Multimedia('capital_128x128.png', Multimedia.LOGO_UNRESTRICTED, width=128, height=128, content='image/png'))
service.media.append(Multimedia('capital_320x240.png', Multimedia.LOGO_UNRESTRICTED, width=320, height=240, content='image/png'))

service.lookup = 'http://capitalfm.com/london'

info.services.append(service)

ensemble = Ensemble(0xe1, 0xcfff)

print marshall(info, ensemble=ensemble)
