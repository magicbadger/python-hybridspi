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
from spi.xml import marshall
import datetime

info = GroupInfo()
groups = ProgrammeGroups(originator='Global Radio', created=datetime.datetime(2014, 4, 25, 14, 21, 15, 0))
info.groupings.append(groups)

group = ProgrammeGroup('crid://www.classicfm.com/shows/tour', 3451, type=ProgrammeGroup.SHOW, numOfItems=24)
group.names.append(MediumName('Musical Tour'))
group.names.append(LongName('Classic\'s Magical Musical Tour'))
group.descriptions.append(ShortDescription('Every Saturday night, join us on a Magical Musical Tour of all things classical music.'))
group.genres.append('urn:tva:metadata:cs:ContentCS:2009:3.6.1')
group.genres.append('urn:tva:metadata:cs:FormatCS:2002:2.5')
group.genres.append('urn:tva:metadata:cs:IntentionCS:2005:1.1')

group.memberships.append(Membership('crid://www.classicfm.com/shows/weekend', 122751))

groups.groups.append(group)


print marshall(info, indent='\t')
