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

def cmd_oboobs(raw_in):
	try:
		data = json.loads(load_page('http://api.oboobs.ru/noise/1/'))[0]
		photo_url = "http://media.oboobs.ru/%s" % data['preview']
		kbd = {"inline_keyboard": [[{'text': 'Another one', 'callback_data': 'oboobs'}]]}
		send_photo(raw_in, photo_url, custom={'reply_markup': json.dumps(kbd)})
	except:
		msg = 'Error!'
		send_msg(raw_in, msg)

def cmd_obutts(raw_in):
	try:
		data = json.loads(load_page('http://api.obutts.ru/noise/1/'))[0]
		photo_url = "http://media.obutts.ru/%s" % data['preview']
		kbd = {"inline_keyboard": [[{'text': 'Another one', 'callback_data': 'obutts'}]]}
		send_photo(raw_in, photo_url, custom={'reply_markup': json.dumps(kbd)})
	except:
		msg = 'Error!'
		send_msg(raw_in, msg)

commands = [['oboobs', cmd_oboobs, False, 'raw', 'Show random picture from oboobs.ru'],
			['obutts', cmd_obutts, False, 'raw', 'Show random picture from obutts.ru']]

# The end is near!
