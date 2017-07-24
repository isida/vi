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

def raw_bot_restart(raw_in, msg, status):
	global GAME_OVER, BOT_EXIT_TYPE, MAX_TIMEOUT
	GAME_OVER = True
	BOT_EXIT_TYPE = status
	MAX_TIMEOUT = 0.001
	send_msg(raw_in, msg)
	#check_updates()

def cmd_update(raw_in):
	raw_bot_restart(raw_in, 'Let\'s update!', 'update')
	
def cmd_restart(raw_in):
	raw_bot_restart(raw_in, 'Let\'s restart!', 'restart')

def cmd_quit(raw_in):
	raw_bot_restart(raw_in, 'See Ya!', 'exit')

def cmd_last_update(raw_in):
	try:
		msg = '🔄 Last update log:\n<pre>%s</pre>' % html_escape_soft(readfile(updatelog_file))
	except:
		msg = 'Update log not found.'
	send_msg(raw_in, msg)

commands = [['update', cmd_update, True, 'raw', 'Update bot from repository.'],
			['restart', cmd_restart, True, 'raw', 'Restart bot.'],
			['quit', cmd_quit, True, 'raw', 'Shutdown bot.'],
			['last', cmd_last_update, False, 'raw', 'Show last update info.']]

# The end is near!
