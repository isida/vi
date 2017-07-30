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

HTML_BODY = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<link href="../../../.css/chatlog.css" rel="stylesheet" type="text/css" />
		<title>CHATNAME - DATE</title>
	</head>
	<body>
		<div class="main">
			<div class="top">
				<div class="link">
				Logs by <a href="https://t.me/isida_bot" class="title-link" target="_blank">@isida_bot</a>
				</div>
				<div class="chat">CHATNAME - DATE</div>
				</div>
				<div class="container">
				BODY
			</div>
		</div>
	</body>
</html>'''

CONFIG_LOG = 'log'

CHAT_ID = {}
LOGGER = True
LOG_FOLDER = DATA_FOLDER % 'chatlog/%s'

try:
	LOG_URL = CONFIG.get(CONFIG_LOG, 'url').strip(' /')
except:
	LOG_URL = None
try:
	LOG_DEBUG = get_config_bin(CONFIG, CONFIG_LOG, 'debug')
except:
	LOG_DEBUG = False

if not os.path.exists(LOG_FOLDER % ''):
	os.mkdir(LOG_FOLDER % '')

def cmd_log(raw_in, text):
	if LOG_URL:
		chat_id = raw_in['message'].get('chat', {}).get('id', '')
		msg = 'Logs are <a href="%s/%s/">here</a>!' % (LOG_URL, chat_id)
	else:
		msg = 'Logs not configured!'
	send_msg(raw_in, msg, custom={'disable_web_page_preview': 'true'})

def logger_self(msg):
	if LOG_DEBUG:
		pprint(json.dumps(msg, indent=2, separators=(',', ': ')), 'green')
	raw_in = {'message': {'chat': {'id': msg['chat_id']}}}
	raw_in['message']['chat']['username'] = BOT_NAME
	raw_in['message']['text'] = msg.get('text', '')
	raw_in['message']['photo'] = msg.get('photo', '')
	raw_in['message']['parse_mode'] = msg.get('parse_mode', '')
	raw_in['message']['custom'] = msg.get('custom', {})
	logger(raw_in)

def replace_items_regexp(t):
	t = t.group().strip(' @')
	return '<a href="https://t.me/%s" target="_blank">@%s</a>' % (t, t)
	
def replace_items(text):
	return re.sub('@[\w]+', replace_items_regexp, text)
	
def logger(raw_in):
	global CHAT_ID
	if LOG_DEBUG:
		pprint(json.dumps(raw_in, indent=2, separators=(',', ': ')), 'yellow')
	if raw_in.has_key('callback_query'):
		RAW_IN = {'message': raw_in['callback_query'].get('message', {})}
		RAW_IN['message']['text'] = '📄 %s' % raw_in['callback_query'].get('data', 'unknown_cmd')
		raw_in = RAW_IN
	FOLDER = '%s' % raw_in['message'].get('chat', {}).get('id', None)
	if FOLDER:
		DATE = ['%02d' % t for t in time.localtime()[:3]]
		FOLDER_RAW = '%s/%s/.template' % (FOLDER, '/'.join(DATE[:-1]))
		if os.path.exists(LOG_FOLDER % FOLDER_RAW) and time.localtime(os.path.getctime(LOG_FOLDER % FOLDER_RAW))[2] != time.localtime()[2]:
			os.remove(LOG_FOLDER % FOLDER_RAW)
		FOLDER_HTML = '%s/%s.html' % (FOLDER, '/'.join(DATE))
		if not os.path.exists(LOG_FOLDER % FOLDER):
			os.mkdir(LOG_FOLDER % FOLDER)
		FOLDER += '/%s' % DATE[0]
		if not os.path.exists(LOG_FOLDER % FOLDER):
			os.mkdir(LOG_FOLDER % FOLDER)
		FOLDER += '/%s' % DATE[1]
		if not os.path.exists(LOG_FOLDER % FOLDER):
			os.mkdir(LOG_FOLDER % FOLDER)
		TYPE = raw_in['message'].get('chat', {}).get('type', '')
		if TYPE in ['private', '']:
			_TYPE = 'chat'
		elif raw_in['message'].has_key('left_chat_participant'):
			_TYPE = 'left_chat_participant'
		elif raw_in['message'].has_key('new_chat_participant'):
			_TYPE = 'new_chat_participant'
		else:
			_TYPE = 'from'
		USERNAME = raw_in['message'].get(_TYPE, {}).get('username', '')
		FIRSTNAME = raw_in['message'].get(_TYPE, {}).get('first_name', '')
		LASTNAME = raw_in['message'].get(_TYPE, {}).get('last_name', '')
		if USERNAME or FIRSTNAME or LASTNAME:
			TIME = ':'.join('%02d' % t for t in time.localtime()[3:6])
			TIME = '<a id="%s" name="%s" href="#%s" class="time">%s</a>' % (TIME, TIME, TIME, TIME)
			if USERNAME:
				NAME = '<a href="https://t.me/%s" target="_blank" class="user">%s</a>' % (USERNAME, USERNAME)
				if FIRSTNAME or LASTNAME:
					NAME += ' </span><span class="name">%s' % ' '.join([FIRSTNAME, LASTNAME])
			else:
				NAME = ' '.join([FIRSTNAME, LASTNAME])
			if _TYPE == 'left_chat_participant':
				TEXT = 'leave chat'
				data = '<span class="time">%s</span> <span class="user-leave">%s</span> <span class="text-leave">%s</span><br />\n' % (TIME, NAME, TEXT)
			elif _TYPE == 'new_chat_participant':
				TEXT = 'join chat'
				data = '<span class="time">%s</span> <span class="user-join">%s</span> <span class="text-join">%s</span><br />\n' % (TIME, NAME, TEXT)
			else:
				TEXT = raw_in['message'].get('text', '').replace('\n', '<br />')
				if not TEXT:
					if raw_in['message'].has_key('sticker'):
						TEXT = '%s [Sticker]' % raw_in['message'].get('sticker',{}).get('emoji', '?')
					elif raw_in['message'].has_key('document'):
						TEXT = '📄 [Document]'
					else:
						IMG = raw_in['message'].get('photo', '')
						if IMG and type(IMG) == type(u''):
								TEXT = '🖼<br /><img class="image" src="%s" alt="" />' % IMG
				else:
					TEXT = replace_items(TEXT)
				data = '<span class="time">%s</span> <span class="user">%s</span> <span class="text">%s</span><br />\n' % (TIME, NAME, TEXT)
			fp = file(LOG_FOLDER % FOLDER_RAW, 'a')
			fp.write(data)
			fp.close()
			data_all = readfile(LOG_FOLDER % FOLDER_RAW)
			chat_id = raw_in['message'].get('chat', {}).get('id', '')
			if TYPE in ['supergroup', 'private']:
				if TYPE == 'supergroup':
					CHAT_TITLE = raw_in['message'].get('chat', {}).get('title', '')
				else:
					CHAT_TITLE = ' '.join([FIRSTNAME, LASTNAME])
				CHAT_NAME = raw_in['message'].get('chat', {}).get('username', '')
				CHAT_ID[chat_id] = [CHAT_TITLE, CHAT_NAME]
			CHAT_TITLE = CHAT_ID.get(chat_id,[''])[0]
			CHAT_NAME = CHAT_ID.get(chat_id,['', ''])[1]
			if CHAT_NAME:
				CHAT_TITLE += ' - <a href="https://t.me/%s" class="title-link" target="_blank">@%s</a>' % (CHAT_NAME, CHAT_NAME)
			HB = HTML_BODY.replace('CHATNAME', CHAT_TITLE)
			_DATE = '<a href="../.." class="title-link">%s</a>/<a href=".." class="title-link">%s</a>/%s' % tuple(DATE)
			HB = HB.replace('DATE', _DATE)
			HB = HB.replace('BODY', data_all)
			writefile(LOG_FOLDER % FOLDER_HTML, HB)

commands = [['log', cmd_log, False, 'all', 'Show log info']]

# The end is near!
