#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    iSida bot VI plugin                                                      #
#    Copyright (C) VitaliyS <hetleven@yandex.ua>                              #
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

def cmd_yandex_currency(raw_in):
	data = requests.get('https://yandex.ru').content
	regexp = '''<span.*?>(.+?)</span'''
	data = str(data).split('<span class="inline-stocks__value_inner">')
	r = []
	repl = [
		['\\xe2\\x88\\x92', '-']
	]
	for t in data:
		cur = t.split('<', 1)[0]
		stat = re.findall(regexp, t)[0].split('<', 1)[0]
		for rep in repl:
			stat = stat.replace(rep[0], rep[1])
		r.append([cur, stat])
	r = r[-3:]
	msg = '<b>Yandex rates</b><pre>'
	icons = ['🇺🇸', '🇫🇲', '🛢']
	values = ['R', 'R', '%']
	for n, i in enumerate(zip(icons, values)):
		msg += '\n%s%s %s%s' % (i[0], r[n][0].replace(',', '.'), r[n][1].replace(',', '.'), i[1])
	msg += '</pre>'
	send_msg(raw_in, msg)

commands = [['ycurr', cmd_yandex_currency, False, 'raw', 'Yandex exchange rate']]

# The end is near!
