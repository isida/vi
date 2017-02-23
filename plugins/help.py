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

def cmd_help(raw_in):
	def get_su(t):
		return ['','⚠️'][t]
	IS_OWNER = raw_in['message']['from'].get('id', '') == OWNER_ID
	rez = []
	for cmd in COMMANDS:
		if IS_OWNER:
			rez.append((cmd[0],cmd[4],get_su(cmd[2])))
		elif not cmd[2]:
			rez.append((cmd[0],cmd[4],''))
	rez.sort()
	msg = 'I know commands:\n'
	msg += '\n'.join('/%s - %s %s' % t for t in rez)
	send_msg(raw_in, msg)

commands = [['help', cmd_help, False, 'raw', 'Bot\'s help.']]

# The end is near!
