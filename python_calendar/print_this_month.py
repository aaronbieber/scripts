#!/usr/bin/env python

from this_month import ThisMonth

this_month = ThisMonth('-->')

# Get US holidays.
this_month.add_calendar(
        'http://www.google.com/calendar/feeds/' + \
        'usa__en%40holiday.calendar.google.com/public/full',
        'holiday',
        '*'
        )

# Get my personal events.
this_month.add_calendar(
        'https://www.google.com/calendar/feeds/' + \
        'aaron%40aaronbieber.com/private-' + \
        '<private hash>/full',
        'personal'
        )
 
this_month.print_this_month()

