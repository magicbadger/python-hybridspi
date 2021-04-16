
import sys

from spi.binary import unmarshall

def usage():
    print("USAGE: parse_binary_schedule.py [filename] (or expects stdin)""")

args = sys.argv[1:]
if len(args):
    filename = args[0]
    print('decoding from', filename)
    f = open(filename, 'rb')
else:
    f = sys.stdin

si, ensemble = unmarshall(f)
print('ServiceInformation', si)
print()
print('Ensemble', ensemble)
print(len(si.services), 'service(s)')
for service in si.services:
    print('\t', service.get_name())
    print('\t\t', service.bearers)
