import unittest

from spi import *


class Test(unittest.TestCase):


    def test_long_running_show(self):
        """
        Testing the splitting and restrictions of long running shows.
        
        The XML specification does not allow for the full use of ISO8601 Periods, such 
        that Hours are the largest allowable unit.
        
        The binary specification has a limit of 18h on a show, due to the field used to 
        encode duration
        """
        
        schedule = Schedule()        
        programme = Programme("crid://example.com/programme/123456", 123456)
        
        programme.names.append(MediumName('Long Show'))
        programme.names.append(LongName('This is a very long show indeed'))
        
        location = Location()
        location.times.append(Time(datetime.datetime(2014, 11, 14, 0, 0, 0, 0), datetime.timedelta(days=7)))
        dab_bearer = DabBearer.fromstring('dab:ce1.ce00.c000.0')
        dab_bearer.offset=3000
        location.bearers.append(dab_bearer)
        location.bearers.append(FmBearer(0xe1, 0xce15, 95800, cost=50, offset=0))
        location.bearers.append(IpBearer('http://example.com/streams/programme.mp3', 'audio/mp3', bitrate=128, cost=80, offset=30000))
        programme.locations.append(location)
        
        schedule.programmes.append(programme)

        info = ProgrammeInfo()
        info.schedules.append(schedule)

        
        from spi.xml import marshall as marshall_xml
        print(marshall_xml(info, indent='   ')) # all this tests right now is the ability to render
     

if __name__ == "__main__":
    unittest.main()
