#!/usr/bin/env python

from bs4 import BeautifulSoup
from datetime import date,datetime
import calendar
import urllib2

class ThisMonth:
    """Combine Google calendars and present a list of events.

       Further explanation forthcoming.
       """

    def __init__(self, today_symbol='->'):
        """Class constructor.
        """
        self.__calendars = []
        self.__today_symbol = today_symbol

    def get_calendar_symbols(self):
        calendar_symbols =  { cal['type']: cal['symbol'] 
                              for cal in self.__calendars }

        calendar_symbols['today'] = self.__today_symbol
        return calendar_symbols

    def ordsuffix(self, number):
        """Return a number with its ordinal suffix attached (e.g. 22nd).

        Accepts as a parameter, NUMBER, which is the number for which to 
        return the ordinal string.
        """
        if 4 <= number <= 20 or 24 <= number <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][number % 10 - 1]

        return str(number) + suffix

    def datestring(self, date):
        """Return a date formatted as we desire.

        Accepts one argument, DATE, which is a datetime object.

        Returns a string like "Thursday, the 4th".
        """
        return date.strftime('%A, the ') + self.ordsuffix(int(date.strftime('%d')))

    def get_events(self, calendar_url, event_type):
        """Return the events occurring this month given a Google Calendar base
        URL.

        Accepts as parameters:
          - CALENDAR_URL, which is the base URL of a Google Calendar XML feed. 
            This URL should point to the "full" version of the feed (ending in 
            "/full") and should not include any query string parameters.
          - EVENT_TYPE, a string indicating the type of event, which will be 
            added to each event dictionary with the key "type".

        Returns a list of dictionaries, where each dictionary is a calendar 
        event having the keys "type", "title", and "when". "Type" and "title" 
        are strings, and "when" is a datetime object.
        """
        today = date.today()
        start_min = '%i-%02i-%02iT00:00:00-04:00' % (today.year, today.month, 1)
        start_max = '%i-%02i-%02iT23:59:59-04:00' % (today.year, today.month,
                calendar.monthrange(
                    today.year,
                    today.month)[1]
                )

        events_xml = urllib2.urlopen(
                ('%s?' +
                    'ctz=America/New_York&' +
                    'orderby=starttime&' +
                    'singleevents=true&' +
                    'sortorder=a&' +
                    'fields=entry/title,entry/gd:when&' +
                    'start-min=%s&start-max=%s') % (calendar_url,
                                                    start_min,
                                                    start_max)
                )

        soup = BeautifulSoup(events_xml.read())

        return [
                {
                    'type':  event_type,
                    'title': h.title.string,
                    'when':  datetime.strptime(h.find('gd:when')
                                                .get('starttime')[:10],
                                               '%Y-%m-%d')
                    }
                for h in soup.find_all('entry')
                ]

    def add_calendar(self, calendar_url, type_name, symbol=''):
        self.__calendars.append({ 'url': calendar_url, 'type': type_name,
                                'symbol': symbol })

    def get_this_month(self):
        all_events = [ { 'type': 'today',
                         'title': 'Today',
                         'when': datetime.today() } ]

        for calendar in self.__calendars:
            all_events = all_events + self.get_events(calendar['url'],
                                                      calendar['type']
                                                     )

        all_events = sorted(all_events, key = lambda k: k['when'])

        return all_events

    def print_this_month(self):
        all_events = self.get_this_month()

        calendar_symbols = self.get_calendar_symbols()
        symbol_column_width = max([ len(symbol) for symbol in 
                                    calendar_symbols.values() ])

        format_string = '%' + str(symbol_column_width) + 's %8s%-9s %s'

        for event in all_events:
            day_marker = calendar_symbols[event['type']]
          
            date_string = self.datestring(event['when'])
            print format_string % (day_marker, date_string.split(',')[0],
                  date_string.split(',')[1], event['title'])

# vim: ts=4 sw=4 et tw=78 cc=+2
