#!/usr/bin/env python3
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

def cmd_news(raw_in, text):
	text = text.strip()
	if text.isdigit():
		limit = int(text)
		if limit > 10:
			limit = 10
		elif limit < 1:
			limit = 1
	else:
		limit = 1
	if hasattr(ssl, '_create_unverified_context'):
		ssl._create_default_https_context = ssl._create_unverified_context
	feed = feedparser.parse('https://github.com/isida/vi/commits/master.atom')
	result = []
	for data in feed['entries'][:limit]:
		link = data['links'][0]['href']
		link_name = link.split('/')[-1][:7]
		msg  = '[%04d.%02d.%02d %02d:%02d:%02d]' % data['updated_parsed'][:6]
		msg += ' ' + data['author']
		msg += ' <a href="%s">%s</a>' % (link, link_name)
		msg += '\n' + data['content'][0]['value']
		result.append(msg)
	msg = '\n\n'.join(result)
	print(msg)
	send_msg(raw_in, msg, custom = {'disable_web_page_preview': True})

commands = [['news', cmd_news, False, 'all', 'Show latest bot\'s commit.']]

# The end is near!
