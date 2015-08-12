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

import sys

from spi.binary import unmarshall

def usage():
    print "USAGE: parse_binary_schedule.py [filename] (or expects stdin)"""

args = sys.argv[1:]
if len(args):
    filename = args[0]
    print 'decoding from', filename
    f = open(filename, 'rb')
else:
    f = sys.stdin

si, ensemble = unmarshall(f)
print 'ServiceInformation', si
print
print 'Ensemble', ensemble
print len(si.services), 'service(s)'
for service in si.services:
    print '\t', service.get_name()
    print '\t\t', service.bearers
