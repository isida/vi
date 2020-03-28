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

EVENTS = {}

def make_name(FROM):
	USERNAME = FROM.get('username', '')
	FIRST = FROM.get('first_name', '')
	LAST = FROM.get('last_name', '')
	NAME = ' '.join(t for t in [FIRST, LAST] if t)
	if NAME and USERNAME:
		return '%s [@%s]' % (NAME, USERNAME)
	elif USERNAME:
		return '@%s' % USERNAME
	elif NAME:
		return NAME
	else:
		return 'id%' % FROM['id']

def cmd_event(raw_in, less):
	global EVENTS
	MESSAGE = raw_in.get('message', {})
	CHAT = MESSAGE.get('chat', {})
	if CHAT.get('type', '') in ['supergroup', 'group']:
		if not less and raw_in['message'].has_key('reply_to_message'):
			if raw_in['message']['reply_to_message'].has_key('text'):
				less = raw_in['message']['reply_to_message']['text']
		if less:
			CHAT_ID = CHAT['id']
			FROM = MESSAGE['from']
			USER_ID = FROM['id']
			EVENT_NAME = less.capitalize().replace(' ', '_')
			EVENTS[CHAT_ID] = EVENTS.get(CHAT_ID, {})
			if EVENTS[CHAT_ID].has_key(EVENT_NAME):
				if USER_ID == EVENTS[CHAT_ID][EVENT_NAME]['id']:
					msg = '❎ Event `%s` removed' % EVENT_NAME
					_ = EVENTS[CHAT_ID].pop(EVENT_NAME)
				else:
					name = make_name(EVENTS[CHAT_ID][EVENT_NAME])
					msg = '⛔️ Event `%s` already exists\nCreated by %s' % (EVENT_NAME, name)
			else:
				EVENTS[CHAT_ID][EVENT_NAME] = FROM
				msg = '✅ Created new event `%s`\nUse %s for remove it' % (EVENT_NAME, MESSAGE['text'].lower().replace(' ', '_'))
		else:
			msg = '⚠️ Required parameter missed!'
	else:
		msg = 'Works only in groups!'
	send_msg(raw_in, msg)

def cmd_events(raw_in):
	global EVENTS
	MESSAGE = raw_in.get('message', {})
	CHAT = MESSAGE.get('chat', {})
	if CHAT.get('type', '') in ['supergroup', 'group']:
		CHAT_ID = CHAT['id']
		FROM = MESSAGE['from']
		USER_ID = FROM['id']
		EVENTS[CHAT_ID] = EVENTS.get(CHAT_ID, {})
		if EVENTS[CHAT_ID]:
			msg = []
			for EVENT_NAME in EVENTS[CHAT_ID].keys():
				if USER_ID == EVENTS[CHAT_ID][EVENT_NAME]['id']:
					msg.append('✅ /event_%s' % EVENT_NAME)
				else:
					name = make_name(EVENTS[CHAT_ID][EVENT_NAME])
					msg.append('⛔️ /event_%s - %s' % (EVENT_NAME, name))
			msg.sort()
			msg = '\n'.join(msg)
		else:
			msg = '✅ No events in current group'
	else:
		msg = 'Works only in groups!'
	send_msg(raw_in, msg)

commands = [
	['event', cmd_event, False, 'all', 'Create lock for event'],
	['events', cmd_events, False, 'raw', 'Show current events']
]

# The end is near!
