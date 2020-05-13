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

def turner_raw(to_turn):
	rtab = u'`1234567890-=qwertyuiop[]\\asdfghjkl;\'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?ё1234567890-=йцукенгшщзхъ\фывапролджэячсмитьбю.Ё!"№;%:?*()_+ЙЦУКЕНГШЩЗХЪ/ФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,'
	ltab = u'ё1234567890-=йцукенгшщзхъ\\фывапролджэячсмитьбю.Ё!"№;%:?*()_+ЙЦУКЕНГШЩЗХЪ/ФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,`1234567890-=qwertyuiop[]\asdfghjkl;\'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
	msg = '🔄 '
	for tt in re.findall('\s+[^\s]*', ' ' + to_turn, re.I+re.U):
		if re.findall('\s+(((svn|http[s]?|ftp)(://))|(magnet:\?))', tt, re.S|re.I|re.U):
			msg += tt
		else:
			msg += ''.join([ltab[rtab.find(x)] if x in rtab else x for x in tt])
	msg = msg.strip()
	return msg

def cmd_turn(raw_in, less):
	if not less and 'reply_to_message' in raw_in['message']:
		if 'text' in raw_in['message']['reply_to_message']:
			less = raw_in['message']['reply_to_message']['text']
	if less:
		msg = turner_raw(less)
	else:
		msg = '⚠️ Required parameter missed!'
	send_msg(raw_in, msg)

commands = [['turn', cmd_turn, False, 'all', 'Turn text from one layout to another.']]

# The end is near!
