from spi import *
from spi.binary import marshall

start = datetime.datetime(2014, 4, 25, 6, 0, 0)
end = datetime.datetime(2014, 4, 25, 13, 0, 0)
schedule = Schedule(start, end, originator='Global Radio')
info = ProgrammeInfo()
info.schedules.append(schedule)

# programme
programme = Programme('crid://www.capitalfm.com/4772/1190223', 1190223)

programme.names.append(ShortName('B\'fast'))
programme.names.append(MediumName('Breakfast'))
programme.names.append(LongName('Capital Breakfast'))
programme.names.append(LongName('Petit-déjeuner de la capitale', language='fr'))
programme.names.append(LongName('キャピタルブレックファースト', language='jp'))
programme.names.append(LongName('დედაქალაქის საუზმე', language='ka'))

location = Location()
location.times.append(Time(datetime.datetime(2014, 4, 25, 6, 0, 0, 0), datetime.timedelta(hours=4), 
                           actual_time=datetime.datetime(2014, 4, 25, 6, 0, 0, 0), actual_duration=datetime.timedelta(hours=4)))
programme.locations.append(location)

programme.descriptions.append(ShortDescription('Forget the coffee, Capital gives you the perfect morning pick-me- up with a blend of the latest hits, travel news and incomparable morning banter.'))

programme.genres.append(Genre('urn:tva:metadata:cs:ContentCS:2002:3.6.8'))
programme.genres.append(Genre('urn:tva:metadata:cs:IntentionCS:2002:1.1'))

programme.memberships.append(Membership('crid://www.capitalfm.com/4772', 4772))

programme.links.append(Link('mailto:capital.breakfast@capitalfm.com', description='Email the Capital Breakfast team!'))
programme.links.append(Link('http://www.capitalfm.com/on-air/breakfast-show/'))

event = ProgrammeEvent('crid://thisisglobal.com/4772/1190223/788946', 788946)
event.names.append(ShortName('Pun'))
event.names.append(MediumName('No.1 Pun'))
event.names.append(LongName('London\'s No. 1 Pun'))
event_location = Location(times=[RelativeTime(datetime.timedelta(hours=3, minutes=10), datetime.timedelta(minutes=25))])
event.locations.append(event_location)
event.descriptions.append(ShortDescription('Can you come up with London\'s No.1 Pun for our story of the day?'))
event.descriptions.append(ShortDescription('Pouvez-vous proposer le jeu de mots n ° 1 de Londres pour notre histoire du jour?', language='fr'))
event.descriptions.append(ShortDescription('今日の私たちの物語のためにロンドンのNo.1しゃれを思い付くことができますか？', language='jp'))
event.descriptions.append(ShortDescription('შეგიძიათ გამოხვიდეთ ლონდონის No.1 პენრით ჩვენი დღის ამბისთვის?', language='ka'))
programme.events.append(event)

schedule.programmes.append(programme)

import sys
sys.stdout.buffer.write(marshall(info))