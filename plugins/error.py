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

def cmd_show_error(raw_in, text):
	if text.lower().strip() == 'clear':
		writefile(LOG_FILENAME, '')
	try:
		cmd = int(text)
	except:
		cmd = 1
	if os.path.isfile(LOG_FILENAME) and text.lower().strip() != 'clear':
		log = readfile(LOG_FILENAME).decode('UTF')
		log = log.split('ERROR:')
		log_len = len(log)
		if cmd > log_len:
			cmd = log_len
		if log_len > 1:
			msg = '🐞 Total Error(s): %s' % (log_len - 1)
			if text != '':
				msg += '\n%s' % '\n'.join('<pre>%s</pre>' % html_escape_soft(t) \
					for t in log[log_len-cmd:log_len])
		else:
			msg = '👍🏻 No Errors!'
	else:
		msg = '👍🏻 No Errors!'
	send_msg(raw_in, msg)

commands = [['error', cmd_show_error, True, 'all', 'Show errors.']]

# The end is near!
