import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'forevents.settings')

import django
django.setup()


from foreventsapp.models import Event, Booking, AppUser
from datetime import date, datetime, time
from django.contrib.auth.models import User

def populate():

    

    pop_events = [
        {'event_title': 'Frank Ocean Never Drops Tour, Glasgow 2025',
         'event_date' : date(2025, 11, 29),
         'venue' : 'OVO Hydro',
         'city' : 'Glasgow',
         'start_time': time(19, 00, 00),
         'artist' : AppUser.objects.get(stage_name='Frank Ocean'),
         'capacity': 14000,
         'date_added': datetime.now()
        },
        {'event_title': 'SZA SOS Tour, London 2025',
         'event_date' : date(2025, 6, 11),
         'venue' : 'O2 Arena',
         'city' : 'London',
         'start_time': time(18, 00, 00),
         'artist' : AppUser.objects.get(stage_name='SZA'),
         'capacity': 20000,
         'date_added': datetime.now()
        },
        {'event_title': 'Tyler the Creator Chromakopia Tour, Berlin 2025',
         'event_date' : date(2025, 8, 4),
         'venue' : 'Uber Arena',
         'city' : 'Berlin',
         'start_time': time(19, 30, 00),
         'artist' : AppUser.objects.get(stage_name='Tyler the Creator'),
         'capacity': 17000,
         'date_added': datetime.now()
        },
        {'event_title': 'Brent Faiyaz Wasteland Tour, Glasgow 2025',
         'event_date' : date(2025, 10, 21),
         'venue' : 'O2 Academy',
         'city' : 'Glasgow',
         'start_time': time(20, 00, 00),
         'artist' : AppUser.objects.get(stage_name='Brent Faiyaz'),
         'capacity': 20000,
         'date_added': datetime.now()
        },
        {'event_title': 'Kehlani Crash Tour, Lisbon 2025',
         'event_date': date(2025, 8, 16),
         'venue': 'O2 Arena',
         'city': 'Lisbon',
         'start_time': time(20, 30, 00),
         'artist': User.objects.get(stage_name='Kehlani'),
         'capacity': 20000,
         'date_added': datetime.now()
        }]
    
    for ev in pop_events:
        add_event(
            ev['event_title'],
            ev['event_date'],
            ev['venue'],
            ev['city'],
            ev['start_time'],
            ev['artist'],
            ev['capacity'],
            ev['date_added'])
    
def add_event(evnt_title, evnt_date, venue, city, start, artst, cap, added):
    e = Event.objects.get_or_create(event_title = evnt_title,
                                    event_date=evnt_date,
                                    venue=venue,
                                    city=city,
                                    start_time=start,
                                    artist=artst,
                                    capacity=cap,
                                    date_added=added)[0]
    e.save()
    return e

if __name__ == '__main__':
    print("Populating 4events database...")
    populate()
    
