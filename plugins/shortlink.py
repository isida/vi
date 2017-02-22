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

SHORT_TINYURL = 'http://tinyurl.com/api-create.php?url=%s'
SHORT_CLCK = 'http://clck.ru/--?url=%s'
SHORT_QR = 'http://chart.apis.google.com/chart?cht=qr&chs=350x350&chld=M|2&chl=%s'

def shorter_raw(raw_in, text, url):
	text = text.strip()
	if text:
		msg = load_page(url % enidna(text).decode('utf-8'))
	else:
		msg = 'What?'
	send_msg(raw_in, msg)

def cmd_short_clck(raw_in, text):
	shorter_raw(raw_in, text, SHORT_CLCK)

def cmd_short_tinyurl(raw_in, text):
	shorter_raw(raw_in, text, SHORT_TINYURL)

def cmd_short_qr(raw_in, text):
	shorter_raw(raw_in, text, SHORT_TINYURL % SHORT_QR)

commands = [['clck', cmd_short_clck, False, 'less', 'URL Shortener'],
			['tinyurl', cmd_short_tinyurl, False, 'less', 'URL Shortener'],
			['qr', cmd_short_qr, False, 'less', 'QR-code generator']]

# The end is near!
