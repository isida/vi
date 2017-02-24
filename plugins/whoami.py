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

def cmd_whoami(raw_in):
	msg =    '🗃 Username: <b>%s</b>' % raw_in['message']['from'].get('username','')
	msg += '\n📰 Name: <b>%s</b>' % raw_in['message']['from'].get('first_name','')
	msg += ' <b>%s</b>' % raw_in['message']['from'].get('last_name','')
	msg += '\n🗂 ID: <b>%s</b>' % raw_in['message']['from'].get('id','')
	IS_OWNER_TXT = ['No','Yes'][raw_in['message']['from'].get('id','') == OWNER_ID]
	msg += '\n🤖 Bot\'s owner: <b>%s</b>' % IS_OWNER_TXT

	send_msg(raw_in,msg)

# name, proc, is_owner, data_type
commands = [['whoami', cmd_whoami, False, 'raw', 'Show info about you.']]

# The end is near!
