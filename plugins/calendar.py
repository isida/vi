#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    iSida bot VI plugin                                                      #
#    Copyright (C) diSabler <dsy@dsy.name>                                    #
#    Copyright (C) dr.Schmurge <dr.schmurge@isida-bot.com>                    #
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                             #
# --------------------------------------------------------------------------- #

def cmd_calendar(raw_in, text):
	text = text.split()
	try:
		month = int(text[0])
	except:
		month = tuple(time.localtime())[1]
	try:
		year = int(text[1])
	except:
		year = tuple(time.localtime())[0]

	msg = '📅 %s' % (timeadd(datetime.datetime.now()))
	msg += '\n<pre>Mo Tu We Th Fr Sa Su\n'
	msg += '\n'.join([' '.join([['%2d' % r, '  '][r==0] for r in t]) for t in calendar.monthcalendar(year, month)])
	msg += '</pre>'

	send_msg(raw_in, msg)

commands = [['calendar', cmd_calendar, False, 'all', 'Calendar [month][year]']]

# The end is near!
