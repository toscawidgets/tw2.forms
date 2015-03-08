"""
The MIT License

Copyright (c) 2007 MVP Sport Systems, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Portions of this document have been taken in part and modified from the
original tw.forms codebase written primarily by Alberto Valaverde


Note that you can not set different languages for multiple calendar widgets
on one page.

TODO: HTML5 type attribute support with native support detection and fallback
"""
import os
import re
from datetime import datetime
import time
import logging

import tw2.core as twc
from .widgets import FormField


__all__ = [
    "CalendarBase",
    "CalendarDatePicker",
    "CalendarDateTimePicker",
    "calendar_js",
    "calendar_setup",
]


# For better calendar widget detection in sprox
class CalendarBase(object):
    '''Base class for calendar widgets'''
    pass


_illegal_s = re.compile(r"((^|[^%])(%%)*%s)")


def _findall(text, substr):
    # Also finds overlaps
    sites = []
    i = 0
    while 1:
        j = text.find(substr, i)
        if j == -1:
            break
        sites.append(j)
        i = j + 1
    return sites


def strftime_before1900(dt, fmt):
    """
    A strftime implementation that supports proleptic Gregorian dates before
    1900.

    @see: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/306860
    """
    if _illegal_s.search(fmt):
        raise TypeError("This strftime implementation does not handle %s")
    if dt.year > 1900:
        return dt.strftime(fmt)

    year = dt.year
    # For every non-leap year century, advance by
    # 6 years to get into the 28-year repeat cycle
    delta = 2000 - year
    off = 6 * (delta // 100 + delta // 400)
    year = year + off

    # Move to around the year 2000
    year = year + ((2000 - year) // 28) * 28
    timetuple = dt.timetuple()
    s1 = time.strftime(fmt, (year,) + timetuple[1:])
    sites1 = _findall(s1, str(year))

    s2 = time.strftime(fmt, (year + 28,) + timetuple[1:])
    sites2 = _findall(s2, str(year + 28))

    sites = []
    for site in sites1:
        if site in sites2:
            sites.append(site)

    s = s1
    syear = "%4d" % (dt.year,)
    for site in sites:
        s = s[:site] + syear + s[site + 4:]
    return s

log = logging.getLogger(__name__)

calendar_css = twc.CSSLink(
    modname='tw2.forms', filename='static/calendar/calendar-system.css')
calendar_js = twc.JSLink(
    modname='tw2.forms', filename='static/calendar/calendar.js')
calendar_setup = twc.JSLink(resources=[calendar_js],
    modname='tw2.forms', filename='static/calendar/calendar-setup.js')

_calendar_lang_re = re.compile(r'^calendar-(\S+).js$')

calendar_langs = dict(
    (_calendar_lang_re.match(f).group(1),
        twc.JSLink(modname=__name__, filename=os.path.join('static/calendar/lang', f)))
    for f in os.listdir(os.path.join(os.path.dirname(__file__), 'static/calendar/lang'))
        if f.startswith('calendar-')
)


class CalendarDatePicker(FormField, CalendarBase):
    """
    Uses a javascript calendar system to allow picking of calendar dates.
    The date_format is in yyyy-mm-dd unless otherwise specified
    """
    template = "tw2.forms.templates.calendar"
    calendar_lang = twc.Param("Default Language to use in the Calendar",
                              default='en')
    required = twc.Param(default=False)
    button_text = twc.Param("Text to display on Button", default="Choose")
    date_format = twc.Param("Date Display Format", default="%Y-%m-%d")
    picker_shows_time = twc.Param('Picker Shows Time', default=False)
    tzinfo = twc.Param('Time Zone Information', default=None)
    setup_options = twc.Param('Calendar.setup(...) options', default={})
#    validator = None
    default = twc.Param(
        'Default value (datetime) for the widget.  If set to a function, ' +
        'it will be called each time before displaying.',
        default=datetime.now)

    def __init__(self, *args, **kw):
        if self.validator is None:
            self.validator = twc.DateTimeValidator(
                format=self.date_format,
                required=self.required
            )
        super(CalendarDatePicker, self).__init__(*args, **kw)

    @classmethod
    def post_define(cls):
        cls.resources = [calendar_css, calendar_js, calendar_setup,
                         calendar_langs[cls.calendar_lang]]

    def prepare(self):
        super(CalendarDatePicker, self).prepare()
        if not self.value and self.required:
            if callable(self.default):
                self.value = self.default()
            else:
                self.value = self.default
        try:
            self.strdate = self.value.strftime(self.date_format)
        except AttributeError:
            self.strdate = self.value

        calendar_options = {"inputField": self.compound_id,
                            "showsTime": self.picker_shows_time,
                            "ifFormat": self.date_format,
                            "button": "%s_trigger" % self.compound_id}
        calendar_options.update(self.setup_options)
        self.add_call(twc.js_function('Calendar.setup')(calendar_options))


class CalendarDateTimePicker(CalendarDatePicker):
    """
    Use a javascript calendar system to allow picking of calendar dates and
    time.
    The date_format is in yyyy-mm-dd hh:mm unless otherwise specified
    """
    messages = {
        'badFormat': 'Invalid datetime format.',
        'empty': 'Please Enter a Date and Time.',
    }
    date_format = "%Y-%m-%d %H:%M"
    picker_shows_time = True
