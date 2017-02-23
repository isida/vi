#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    iSida bot VI plugin                                                      #
#    Copyright (C) diSabler <dsy@dsy.name>                                    #
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

def cmd_todate(raw_in, text):
	date = re.findall('([\d]+)',text)
	if date:
		day = int(date[0])
		if len(date) > 1:
			month = int(date[1])
		else:
			month = time.localtime()[1]
		if len(date) > 2:
			year = int(date[2])
		else:
			year = time.localtime()[0]
		try:
			_ = time.mktime([year, month, day] + [0] * 6)
			days_remain = (datetime.date(year, month, day) - datetime.date.today()).days
			if days_remain > 0:
				msg = 'To %02d.%02d.%04d remain %s day(s).' % (day, month, year, days_remain)
			elif days_remain < 0:
				msg = '%02d.%02d.%04d was %s day(s) ago.' % (day, month, year, int(days_remain))
			else:
				msg = '%02d.%02d.%04d is now!' % (day, month, year)
		except:
			msg = 'Wrong date.'			
	else:
		msg = 'Need date.'
	send_msg(raw_in, msg)

commands = [['todate', cmd_todate, False, 'all', 'Days to date. Day [Month] [Year]']]

# The end is near!
