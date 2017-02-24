#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    iSida bot VI plugin                                                      #
#    Copyright (C) diSabler <dsy@dsy.name>                                    #
#    Copyright (C) ferym <ferym@jabbim.org.ru>                                #
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

horodb  = ['aries', 'taurus', 'gemini', 'cancer', \
           'leo', 'virgo', 'libra', 'scorpio', \
		   'sagittarius', 'capricorn', 'aquarius', 'pisces']
horoemo = ['♈️', '♉️', '♊️', '♋️', '♌️', '♍️', '♎️', '♏️', '♐️', '♑️', '♒️', '♓️']

horo_dates = ['21.03-19.04', '20.04-20.05', '21.05-20.06', \
			  '21.06-22.07', '23.07-22.08', '23.08-22.09', \
			  '23.09-22.10', '23.10-21.11', '22.11-21.12', \
			  '22.12-19.01', '20.01-18.02', '19.02-20.03']

def cmd_horoscope(raw_in, text):
	param = text.strip().lower()
	msg = 'What?'
	if param:
		if param == 'list':
			msg = '\n'.join(['%s %s' % \
                (horoemo[i], t.capitalize()) for i,t in enumerate(horodb)])
		if param == 'date':
			msg = 'List of dates:\n%s' % '\n'.join(['%s … %s %s' % \
                (horo_dates[i], horoemo[i], t.capitalize()) for i,t in enumerate(horodb)])
		if param in horodb:
			body = html_encode(load_page('http://horo.mail.ru/prediction/%s/today' % param))
			try:
				msg = '%s %s (%s)\n%s' % (horoemo[horodb.index(param)], \
					param.capitalize(), \
					horo_dates[horodb.index(param)], \
					unhtml_hard(re.findall('<div class="article__item.*?>(.+?)</div>',body,re.S|re.I|re.U)[0].strip()))
			except:
				raise
				msg = 'Unknown error!'
	send_msg(raw_in, msg)

commands = [['horo', cmd_horoscope, False, 'all', 'Horoscope. List|Date.']]

# The end is near!
