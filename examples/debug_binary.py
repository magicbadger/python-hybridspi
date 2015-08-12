import logging
import sys
from bitarray import bitarray
from spi.binary import Element, Attribute
from collections import OrderedDict as od
from asciitree import LeftAligned
from asciitree.traversal import Traversal, AttributeTraversal

logger = logging.getLogger('binary_decoder')

def usage():
    print "USAGE: parse_binary_schedule.py [filename] (or expects stdin)"""

args = sys.argv[1:]
if len(args):
    filename = args[0]
    print 'decoding from', filename
    f = open(filename, 'rb')
else:
    f = sys.stdin

b = bitarray()
if isinstance(f, file):
    logger.debug('object is a file')
    import StringIO
    io = StringIO.StringIO()
    d = f.read()
    while d:
        io.write(d)
        d = f.read()
    b.frombytes(io.getvalue())
else:
    logger.debug('object is a string of %d bytes', len(str(i)))
    b.frombytes(f)

e = Element.frombits(b)

class ElementTraversal(Traversal):

    def get_children(self, node):
        if isinstance(node, Element): 
            children = node.attributes + node.children
            if node.cdata: children.append(node.cdata)
            return children
        else: return []

    def get_text(self, node):
        if isinstance(node, Element):
            return 'Element 0x%02x' % node.tag
        elif isinstance(node, Attribute):
            return 'Attribute 0x%02x : %s' % (node.tag, str(node.value))
        else:
            return str(node)

l = LeftAligned(traverse=ElementTraversal())
print l(e)
