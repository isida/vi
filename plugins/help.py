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

def get_su(t):
	return ['', '⚠️'][t]

def cmd_help(raw_in, text):
	IS_OWNER = raw_in['message']['from'].get('id', '') in OWNER_ID
	text = text.lower().strip()
	if not text:
		msg = ['🤖 iSida telegram bot',
			   '(c) 2oo9-%s Disabler Production Lab.' % str(time.localtime()[0]).replace('0', 'o'),
			   '🔸 Available commands list: /commands',
			   '🔸 Help list: /help_list',
			   '🔸 Help all commands: /help_all',
			   '🔸 Dev-chat @isida_bot_dev',
			   '🔸 Site: http://isida.dsy.name']
		msg = '\n'.join(msg)
		send_msg(raw_in, msg, custom = {'disable_web_page_preview': True})
	else:
		rez = []
		if text == 'list':
			for cmd in COMMANDS:
				if IS_OWNER or not cmd[2]:
					if IS_OWNER:
						rez.append((cmd[0], get_su(cmd[2])))
					else:
						rez.append((cmd[0], ''))
			msg = '\n'.join('/help_%s %s' % t for t in rez)
		else:
			if text == 'all':
				text = ''
			for cmd in COMMANDS:
				if (text in cmd[0].lower() or text in cmd[4].lower()) \
					and (IS_OWNER or not cmd[2]):
					if IS_OWNER:
						rez.append((cmd[0], cmd[4], get_su(cmd[2])))
					else:
						rez.append((cmd[0], cmd[4], ''))
			if rez:
				msg = '\n'.join('/%s - %s %s' % t for t in rez)
				msg = msg.replace('  ', ' ').strip()
			else:
				msg = 'Not found.'
		send_msg(raw_in, msg)

def cmd_commands(raw_in):
	IS_OWNER = raw_in['message']['from'].get('id', '') in OWNER_ID
	try:
		CHAT_ID = raw_in['message']['chat'].get('id', 0)
	except:
		CHAT_ID = 0
	rez = []
	for cmd in COMMANDS:
		if CHAT_ID not in cmd[5].get('black', []) and not ('white' in cmd[5] and CHAT_ID not in cmd[5].get('white', [])):
			if IS_OWNER:
				rez.append((cmd[0], get_su(cmd[2])))
			elif not cmd[2]:
				rez.append((cmd[0], ''))
	rez.sort()
	msg = 'I know commands:\n'
	msg += ' | '.join('/%s %s' % t for t in rez)
	msg = msg.replace('  ', ' ').strip()
	send_msg(raw_in, msg)

def cmd_start(raw_in):
	msg = ['🤖 Hi! I\'m iSida, telegram bot. Ex jabber bot.',
		   'Use /help for begin.',
		   'Join dev-chat @isida_bot_dev']
	msg = '\n'.join(msg)
	send_msg(raw_in, msg)

commands = [['help', cmd_help, False, 'all', 'Bot\'s help.'],
			['start', cmd_start, False, 'raw', 'Bot\'s begin info.'],
			['commands', cmd_commands, False, 'raw', 'Bot\'s commands list.']]

# The end is near!
