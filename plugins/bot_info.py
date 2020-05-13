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

def cmd_bot_info(raw_in):
	msg = '🤖 %s %s' % (botName, get_bot_version())
	msg += '\n🔄 Cycles: %s' % CYCLES
	msg += '\n▶️ Threads: %s' % THREAD_COUNT
	msg += '\n❗️ Error threads: %s' % THREAD_ERROR_COUNT
	send_msg(raw_in, msg)

commands = [['botinfo', cmd_bot_info, False, 'raw', 'Bot\'s info.']]

# The end is near!
