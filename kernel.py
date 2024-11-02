#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    iSida bot VI                                                             #
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

import datetime
import calendar
import chardet
import configparser
import feedparser
import json
import logging
import math
import os
import requests
import time
import random
import re
import socket
import string
import ssl
import sys
import threading

# Threads with `kill` feature
class KThread(threading.Thread):
	def __init__(self, *args, **keywords):
		threading.Thread.__init__(self, *args, **keywords)
		self.killed = False

	def start(self):
		self.__run_backup = self.run
		self.run = self.__run
		threading.Thread.start(self)

	def __run(self):
		sys.settrace(self.globaltrace)
		self.__run_backup()
		self.run = self.__run_backup

	def globaltrace(self, frame, why, arg):
		if why == 'call':
			return self.localtrace
		else:
			return None

	def localtrace(self, frame, why, arg):
		if self.killed:
			if why == 'line':
				raise SystemExit()
		return self.localtrace

	def kill(self):
		self.killed = True

# Execute new thread
def thr(func, param, name):
	global THREAD_COUNT, THREAD_ERROR_COUNT, sema
	THREAD_COUNT += 1
	try:
		tmp_th = KThread(group=None, target=log_execute,
			name='%s_%s' % (THREAD_COUNT, name), args=(func, param))
		tmp_th.start()
	except SystemExit:
		pass
	except:
		MSG = '\n'.join(str(t) for t in sys.exc_info())
		if 'thread' in MSG.lower():
			THREAD_ERROR_COUNT += 1
		else:
			lt = datetime.datetime.now()
			logging.exception(' [%s] %s' % (timeadd(lt), str(func)))
		try:
			tmp_th.kill()
		except:
			pass
		if HALT_ON_EXCEPTION:
			raise

# Execute with exception catch
def log_execute(proc, params):
	try:
		proc(*params)
	except SystemExit:
		pass
	except:
		lt = datetime.datetime.now()
		logging.exception(' [%s] %s' % (timeadd(lt), str(proc)))

# Soft escape html
def html_escape_soft(text):
	for tmp in (('<', '&lt;'), ('>', '&gt;')):
		text = text.replace(tmp[0], tmp[1])
	return text

# Read file
def readfile(filename):
	with open(filename) as fp:
		data = fp.read()
	fp.close()
	return data

# Write file
def writefile(filename, data):
	with open(filename, 'w') as fp:
		fp.write(data)
	fp.close()

# Get Bot's version
def get_bot_version():
	if os.path.isfile(ver_file):
		bvers = readfile(ver_file).replace('\n', '').\
					replace('\r', '').replace('\t', '').replace(' ', '')
		bV = '%s.%s-%s' % (botVersionDef, bvers, base_type)
	else:
		bV = '%s-%s' % (botVersionDef, base_type)
	return bV

# Get OS version
def get_os_version():
	iSys = sys.platform
	iOs = os.name
	isidaPyVer = '%s [%s]' % (sys.version.split(' (')[0], sys.version.split(')')[0].split(', ')[1])
	if iOs == 'posix':
		osInfo = os.uname()
		isidaOs = '%s %s-%s / Python %s' % (osInfo[0], osInfo[2], osInfo[4], isidaPyVer)
	elif iSys == 'win32':
		def get_registry_value(key, subkey, value):
			import _winreg
			key = getattr(_winreg, key)
			handle = _winreg.OpenKey(key, subkey)
			(value, type) = _winreg.QueryValueEx(handle, value)
			return value
		def get(key):
			return get_registry_value("HKEY_LOCAL_MACHINE", "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", key)
		osInfo = ' '.join(get("ProductName").split()[:3])
		buildInfo = get("CurrentBuildNumber")
		try:
			spInfo = get("CSDVersion")
			isidaOs = '%s %s [%s] / Python %s' % (osInfo, spInfo, buildInfo, isidaPyVer)
		except:
			isidaOs = '%s [%s] / Python %s' % (osInfo, buildInfo, isidaPyVer)
	else:
		isidaOs = 'unknown'
	return isidaOs

# Get color by name on Linux
def get_color(c):
	color = 'TERM' in os.environ
	colors = {'clear':'[0m', 'blue':'[34m', 'red':'[31m', 'magenta':'[35m',
			  'green':'[32m', 'cyan':'[36m', 'brown':'[33m', 'light_gray':'[37m',
			  'black':'[30m', 'bright_blue':'[34;1m', 'bright_red':'[31;1m',
			  'purple':'[35;1m', 'bright_green':'[32;1m', 'bright_cyan':'[36;1m',
			  'yellow':'[33;1m', 'dark_gray':'[30;1m', 'white':'[37;1m'}
	return ['', '\x1b%s' % colors[c]][color]

# Get color by name on Windows
def get_color_win32(c):
	colors = {'clear':7, 'blue':1, 'red':4, 'magenta':5, 'green':2, 'cyan':3,
			  'brown':6, 'light_gray':7, 'black':0, 'bright_blue':9,
			  'bright_red':12, 'purple':13, 'bright_green':10, 'bright_cyan':11,
			  'yellow':14, 'dark_gray':8, 'white':15}
	return colors[c]

# Time and date to string
def timeadd(lt):
	return datetime.datetime.strftime(lt, "%Y.%m.%d %H:%M:%S")

# Time to string
def onlytimeadd(lt):
	return datetime.datetime.strftime(lt, "%H:%M:%S")

# Exclude non-ascii symbols
def parser(t):
	try:
		return ''.join([['?', l][l<='~'] for l in unicode(t)])
	except:
		with open(slog_folder % 'critical_exception_%s.txt' % int(time.time()), 'wb') as fp:
			fp.write(t)
		fp.close()

# Log message
def pprint(*text):
	global last_logs_store
	c, wc, win_color = '', '', ''
	if len(text) > 1:
		if is_win32:
			win_color = get_color_win32(text[1])
		else:
			c, wc = get_color(text[1]), get_color('clear')
	elif is_win32:
		win_color = get_color_win32('clear')
	text = text[0]
	lt = datetime.datetime.now()
	zz = '%s[%s]%s %s%s' % (wc, onlytimeadd(lt), c, text, wc)
	last_logs_store = ['[%s] %s' % (onlytimeadd(lt), text)] + \
						last_logs_store[:last_logs_size]
	if DEBUG_CONSOLE:
		if is_win32 and win_color:
			ctypes.windll.Kernel32.SetConsoleTextAttribute(win_console_color, \
				get_color_win32('clear'))
			print(zz.split(' ', 1)[0],)
			ctypes.windll.Kernel32.SetConsoleTextAttribute(win_console_color, \
				win_color)
			try:
				print(zz.split(' ', 1)[1])
			except:
				print(parser(zz.split(' ', 1)[1]))
			ctypes.windll.Kernel32.SetConsoleTextAttribute(win_console_color, \
				get_color_win32('clear'))
		else:
			try:
				print(zz)
			except:
				print(parser(zz))
	if DEBUG_LOG:
		fname = SYSLOG_FOLDER % datetime.datetime.strftime(lt, "%Y%m%d.txt")
		fbody = '%s|%s\n' % (onlytimeadd(lt), text.replace('\n', '\r'))
		with open(fname, 'a') as fl:
			fl.write(fbody)
		fl.close()

# Error message
def Error(text):
	print('Error! %s' % text)
	sys.exit()

# Get integer value from config
def get_config_int(_config, _section, _name):
	try:
		return int(_config.get(_section, _name))
	except:
		return -1

# Get integer array of values from config
def get_config_int_array(_config, _section, _name):
	try:
		return [int(t) for t in _config.get(_section, _name).split() if t]
	except:
		return [-1]

# Get binary value from config
# True == 1, '1', 'yes', 'true'
# False == all else
def get_config_bin(_config, _section, _name):
	try:
		_var = int(_config.get(_section, _name))
	except:
		_var = _config.get(_section, _name).lower()
	_True = [1, '1', 'yes', 'true']
	return _var in _True

# Replace non-ascii and TAB, CR, LF
def remove_sub_space(t):
	return ''.join([['?', l][l>=' ' or l in '\t\r\n'] for l in str(t)])

# Send request
def send_raw(raw_in, method, dt, fl={}):
	if LOGGER:
		try:
			logger_self(dt)
		except:
			pprint(json.dumps(dt, indent=2, separators=(',', ': ')), 'red')
	request = requests.post(API_URL % method,
							data = dt,
							files = fl,
							proxies = PROXIES)
	if not request.status_code == 200:
		pprint('*** Error code on %s: %s' % (method, request.status_code), 'red')
		pprint('Raw_in dump:\n%s' % json.dumps(raw_in, indent=2, separators=(',', ': ')), 'red')
		pprint('Data dump:\n%s' % json.dumps(dt, indent=2, separators=(',', ': ')), 'red')
		return False
	else:
		return True

# Send message
def send_msg(raw_in, msg, parse_mode = 'HTML', custom={}):
	global RAW_IN
	RAW_IN = raw_in
	#if parse_mode == 'HTML':
	#	msg = html_escape_soft(msg)
	MSG = { 'chat_id': raw_in['message']['chat'].get('id', ''),
			'text': msg,
			'parse_mode': parse_mode }
	MSG.update(custom)
	return send_raw(raw_in, 'sendMessage', MSG)

# Send photo
def send_photo(raw_in, photo, custom={}):
	if re.match('https?://.*\.(jpe?g|png|gif)$', photo.lower()):
		MSG = { 'chat_id': raw_in['message']['chat'].get('id', ''),
		'photo': photo  }
		FLS = {}
	else:
		MSG = { 'chat_id': raw_in['message']['chat'].get('id', '') }
		FLS = {'photo': (photo, open(photo, "rb"))}
	MSG.update(custom)
	return send_raw(raw_in, 'sendPhoto', MSG, FLS)

# Send document
def send_document(raw_in, document, custom={}):
	if re.match('https?://.*\.(pdf|zip|gif)$', document.lower()):
		MSG = { 'chat_id': raw_in['message']['chat'].get('id', ''),
		'document': document  }
		FLS = {}
	else:
		MSG = { 'chat_id': raw_in['message']['chat'].get('id', '') }
		FLS = {'document': (document, open(document, "rb"))}
	MSG.update(custom)
	return send_raw(raw_in, 'sendDocument', MSG, FLS)

# Open web page
def get_opener(page_name, parameters=None):
	socket.setdefaulttimeout(www_get_timeout)
	headers = {
		'User-Agent': USER_AGENT,
		'Cache-Control': 'no-cache'
	}
	try:
		data = requests.get(page_name,
							data = parameters,
							proxies = WEB_PROXIES,
							headers = headers).content
		result = True
	except:
		MSG = '\n'.join(str(t) for t in sys.exc_info())
		data = 'Error! %s' % MSG.replace('>', '').replace('<', '').capitalize()
		result = False
	print(data)
	return data, result

# Load page with limited size
def load_page_size(page_name, page_size, parameters=None):
	data, result = get_opener(page_name, parameters)
	if result:
		return data[:page_size].decode()
	else:
		return data

# Load page without limited size
def load_page(page_name, parameters=None):
	data, result = get_opener(page_name, parameters)
	if result:
		return data[:size_overflow].decode()
	else:
		return data

# Check new incoming messages
def check_updates():
	global OFFSET
	data = {'limit': 0,
			'timeout': POLLING_TIMEOUT}
	if OFFSET:
		data['offset'] = OFFSET + 1

	try:
		request = requests.post(API_URL % 'getUpdates',
								data = data,
								proxies = PROXIES,
								timeout = POLLING_TIMEOUT + MAX_TIMEOUT)
	except requests.exceptions.ReadTimeout:
		pprint('*** Connection timeout on getUpdates. Waiting %s seconds.' % MAX_TIMEOUT, 'red')
		return False
	except requests.exceptions.ConnectionError:
		pprint('*** Connection error on getUpdates. Waiting %s seconds.' % MAX_TIMEOUT, 'red')
		return False

	if not request.status_code == 200:
		pprint('*** Error code on getUpdates: %s' % request.status_code, 'red')
		return False
	if not request.json()['ok']:
		pprint('*** No `ok` json on getUpdates: %s' % request.json(), 'red')
		return False

	for msg_in in request.json()['result']:
		if DEBUG_JSON:
			pprint(json.dumps(msg_in, indent=2, separators=(',', ': ')), 'magenta')
		if OFFSET:
			OFFSET = msg_in['update_id']
		else:
			OFFSET = msg_in['update_id']
			return True
		try:
			if 'message' in msg_in:
				CHAT_ID = msg_in['message']['chat'].get('id', 0)
			elif 'callback_query' in msg_in:
				CHAT_ID = msg_in['callback_query']['message']['chat'].get('id', 0)
			else:
				CHAT_ID = 0
		except:
			CHAT_ID = 0
		if LOGGER:
			try:
				logger(msg_in)
			except:
				pprint(json.dumps(msg_in, indent=2, separators=(',', ': ')), 'red')
		if 'edited_message' in msg_in:
			msg_in['message'] = msg_in['edited_message']
			pprint('*** Edited message!', 'yellow')
		elif 'callback_query' in msg_in:
			msg_in['message'] = msg_in['callback_query']['message']
			msg_in['message']['text'] = msg_in['callback_query']['data']
			pprint('*** Callback query!', 'yellow')

		#send_msg(msg_in, '<i>Edited messages not supported now!</i>')

		if 'message' not in msg_in or 'text' not in msg_in['message']:
			if 'new_chat_participant' in msg_in['message']:
				pprint('New participant|%s' % '|'.join([str(t) for t in [\
					msg_in['message']['chat'].get('all_members_are_administrators', ''), \
					msg_in['message']['chat'].get('type', ''), \
					msg_in['message']['chat'].get('id', ''), \
					msg_in['message']['chat'].get('title', ''), \
					msg_in['message']['new_chat_participant'].get('id', ''), \
					msg_in['message']['new_chat_participant'].get('username', ''), \
					msg_in['message']['new_chat_participant'].get('first_name', ''), \
					msg_in['message']['new_chat_participant'].get('last_name', '') ]]), 'cyan')
				break
			elif 'left_chat_participant' in msg_in['message']:
				pprint('Left participant|%s' % '|'.join([str(t) for t in [\
					msg_in['message']['chat'].get('all_members_are_administrators', ''), \
					msg_in['message']['chat'].get('type', ''), \
					msg_in['message']['chat'].get('id', ''), \
					msg_in['message']['chat'].get('title', ''), \
					msg_in['message']['left_chat_participant'].get('id', ''), \
					msg_in['message']['left_chat_participant'].get('username', ''), \
					msg_in['message']['left_chat_participant'].get('first_name', ''), \
					msg_in['message']['left_chat_participant'].get('last_name', '') ]]), 'cyan')
				break
			else:
				pprint('Unknown message', 'red')
				pprint(json.dumps(msg_in, indent=2, separators=(',', ': ')), 'magenta')
				continue

		IS_OWNER = msg_in['message']['from'].get('id', '') in OWNER_ID
		CMD = msg_in['message'].get('text', '').strip()
		splitter = '<%s>' % random.randint(0, 2 ** 32)
		CMD = CMD.replace(BOT_NAME, splitter)
		CMD = CMD.replace('_', ' ')
		CMD = CMD.replace(splitter, BOT_NAME)
		_ID = msg_in['message']['from'].get('id', '')
		_USERNAME = msg_in['message']['from'].get('username', '')
		_FIRST_NAME = msg_in['message']['from'].get('first_name', '')
		_LAST_NAME = msg_in['message']['from'].get('last_name', '')

		pprint('|'.join([str(t) for t in [_ID, _USERNAME, _FIRST_NAME, \
			_LAST_NAME, CMD]]), 'cyan')
		# name, proc, is_owner, data_type
		#commands = ['whoami', cmd_whoami, False, 'raw']
		# Command parser!
		IS_COMMAND = False
		for c in COMMANDS:
			if c[2] and IS_OWNER:
				ALLOW = True
			elif not c[2]:
				if 'white' in c[5].keys() and CHAT_ID not in c[5]['white']:
					ALLOW = False
				elif 'black' in c[5].keys() and CHAT_ID in c[5]['black']:
					ALLOW = False
				else:
					ALLOW = True
			else:
				ALLOW = False
			if CMD.startswith('/'):
				CMD = CMD[1:]
			if CMD.lower().startswith('%s ' % c[0]) or CMD.lower() == c[0] or \
				CMD.lower() == '%s@%s' % (c[0], BOT_NAME) or \
				CMD.lower().startswith('%s@%s ' % (c[0], BOT_NAME)) or \
				CMD.lower().startswith('@%s %s' % (BOT_NAME, c[0])):
				if ALLOW:
					if c[3] == 'raw':
						thr(c[1], (msg_in, ), CMD)
					elif c[3] in ['less', 'all']:
						less = CMD[len(c[0]):].strip()
						if less.lower().startswith('@%s' % BOT_NAME):
							less = less[len(BOT_NAME)+1:].strip()
						elif less.lower().endswith('@%s' % BOT_NAME):
							less = less[:-(len(BOT_NAME)+1)].strip()
						if c[3] == 'less' and not less:
							send_msg(msg_in, '⚠️ Required parameter missed!')
						else:
							thr(c[1], (msg_in, less), CMD)
				else:
					send_msg(msg_in, '🔒 Locked!')
				IS_COMMAND = True
				break

		if not IS_COMMAND:
			if (msg_in['message']['text'].lower().startswith('@%s ' % BOT_NAME) and \
					'chat' in msg_in['message'] and \
					'type' in msg_in['message']['chat'] and \
					msg_in['message']['chat'].get('type', '') in ['group', 'supergroup']) or \
					('reply_to_message' in msg_in['message'] and \
					'from' in msg_in['message']['reply_to_message'] and \
					'username' in msg_in['message']['reply_to_message']['from'] and \
					msg_in['message']['reply_to_message']['from'].get('username', '').lower() == BOT_NAME):
				text = msg_in['message']['text']
				if text.lower().startswith('@%s ' % BOT_NAME):
					text = text[len(BOT_NAME)+1:].strip()
				pprint('>>> Chat: %s' % text, 'green')
				msg = getAnswer(msg_in, text)
				pprint('<<< Chat: %s' % msg, 'bright_green')
				#time.sleep(len(msg) / 3.0 + random.randint(0, 3))
				send_msg(msg_in, msg)
			elif ('chat' in msg_in['message'] and \
					'type' in msg_in['message']['chat'] and \
					msg_in['message']['chat'].get('type', '') == 'private'):
				text = msg_in['message'].get('text').strip()
				pprint('>>> Chat: %s' % text, 'green')
				msg = getAnswer(msg_in, text)
				pprint('<<< Chat: %s' % msg, 'bright_green')
				#time.sleep(len(msg) / 3.0 + random.randint(0, 3))
				send_msg(msg_in, msg)
			else:
				pass
				#pprint('Unknown message', 'red')
				#pprint(json.dumps(msg_in, indent=2, separators=(',', ': ')), 'magenta')
	return True

def get_tag(body, tag):
	T = re.findall('<%s.*?>(.*?)</%s>' % (tag, tag), body, re.S)
	if T:
		return T[0]
	else:
		return ''

def shell_execute(cmd):
	if PARANOIA_MODE:
		result = '🔒 Command temporary blocked!'
	else:
		tmp_file = '%s.tmp' % int(time.time())
		try:
			error_answ = os.system('%s > %s 2>&1' % (cmd, tmp_file))
			if not error_answ:
				try:
					body = html_escape_soft(readfile(tmp_file))
				except:
					body = '⚠️ Command execution error.'
				if len(body):
					result = remove_sub_space(str(body))
				else:
					result = 'ok'
			else:
				result = '⚠️ Command execution error.'
				try:
					result += '\n' + html_escape_soft(readfile(tmp_file))
				except:
					pass
		except:
			MSG = '\n'.join(str(t) for t in sys.exc_info())
			result = '⚠️ I can\'t execute it! Error: %s' % MSG
		try:
			os.remove(tmp_file)
		except:
			pass
	return '<code>%s</code>' % result

# --- Let's begin! ----------------------------------------------------------- #
TELEGRAM_API_URL   = 'https://api.telegram.org/bot%s' # Bot apt URL
SETTING_FOLDER     = 'settings/%s'                    # Setting folder
PLUGIN_FOLDER      = 'plugins/%s'                     # Plugins folder
DATA_FOLDER        = 'data/%s'                        # Data folder
TMP_FOLDER         = DATA_FOLDER % 'tmp/%s'
ver_file           = TMP_FOLDER % 'version'          # Bot's version file
SYSLOG_FOLDER      = DATA_FOLDER % 'syslog/%s'        # Syslogs folder
CONFIG_FILE        = SETTING_FOLDER % 'config.ini'    # Config filename
LOG_FILENAME       = SYSLOG_FOLDER % 'error.txt'      # Error logs
last_logs_store    = []                               # Last logs
last_logs_size     = 20                               # Last logs count
DEBUG_CONSOLE      = True                             # Show debugging in console
DEBUG_LOG          = True                             # Logging all bot's actions
CONFIG_MAIN        = 'main'                           # Main section name in config
CONFIG_DEBUG       = 'debug'                          # Debug section name in config
CONFIG_OWNER       = 'owner'                          # Owner section name in config
CONFIG_LISTS       = 'lists'                          # White/black lists section name in config
CONFIG_SOCKS_PROXY = 'socks_proxy'                    # Socks proxy section name in config
CONFIG_WEB         = 'web'                            # Web section name in config
botName            = 'iSida'                          # Bot's name
botVersionDef      = '6.2'                            # Bot's version
base_type          = 'NoDB'                           # Bot's base type
www_get_timeout    = 15                               # Timeout for web requests
size_overflow      = 262144                           # Web page limit in bytes
TIMEOUT            = 1                                # Timeout between request updates
MAX_TIMEOUT        = 15                               # Maximal timeout after request error
CYCLES             = 0                                # Work cycles
THREAD_COUNT       = 0                                # Executed threads
THREAD_ERROR_COUNT = 0                                # Threads with error
GAME_OVER          = False                            # Bot's status
BOT_EXIT_TYPE      = ''                               # Reason for bot's kernel exit
LOGGER             = False                            # Logger plugin
POLLING_TIMEOUT    = 30                               # Long polling timeout

# --- Init ------------------------------------------------------------------- #
try:
	_ = OFFSET
except NameError:
	OFFSET = 0
logging.basicConfig(filename=LOG_FILENAME)#, level=logging.DEBUG, )
sema = threading.BoundedSemaphore(value=30)
is_win32 = sys.platform == 'win32'
if is_win32:
	import ctypes
	ctypes.windll.Kernel32.GetStdHandle.restype = ctypes.c_ulong
	win_console_color = ctypes.windll.Kernel32.GetStdHandle(ctypes.c_ulong(0xfffffff5))

pprint('-'*50, 'blue')
pprint('%s %s // %s' % (botName, get_bot_version(), get_os_version()), 'bright_cyan')
pprint('-'*50, 'blue')
pprint('*** Init enviroment succed', 'white')

# --- Config ----------------------------------------------------------------- #
pprint('*** Loading config', 'white')
if not os.path.exists(CONFIG_FILE):
	Error('Config file not found: %s' % CONFIG_FILE)
CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_FILE)
SECTIONS = CONFIG.sections()
if CONFIG_MAIN not in SECTIONS:
	Error('Main options not found in %s' % CONFIG_FILE)
if CONFIG_DEBUG not in SECTIONS:
	Error('Debug options not found in %s' % CONFIG_FILE)
if CONFIG_OWNER not in SECTIONS:
	Error('Owner options not found in %s' % CONFIG_FILE)
if CONFIG_LISTS not in SECTIONS:
	pprint('!!! White/black lists options not found in %s' % CONFIG_FILE, 'red')
if CONFIG_SOCKS_PROXY not in SECTIONS:
	pprint('Socks proxy settings not found in %s' % CONFIG_FILE, 'white')
	PROXIES = {}
else:
	pprint('Read socks proxy settings...', 'white')
	proxy = {}
	proxy['HOST'] = CONFIG.get(CONFIG_SOCKS_PROXY, 'host')
	proxy['PORT'] = CONFIG.get(CONFIG_SOCKS_PROXY, 'port')
	proxy_string = '%(HOST)s:%(PORT)s'
	if CONFIG.has_option(CONFIG_SOCKS_PROXY, 'user'):
		proxy['USER'] = CONFIG.get(CONFIG_SOCKS_PROXY, 'user')
		if CONFIG.has_option(CONFIG_SOCKS_PROXY, 'pass'):
			proxy['PASS'] = ':%s' % CONFIG.get(CONFIG_SOCKS_PROXY, 'pass')
		else:
			proxy['PASS'] = ''
		proxy_string = '%(USER)s%(PASS)s@' + proxy_string
	proxy_string = 'socks5://' + proxy_string
	PROXIES = {'http':  proxy_string % proxy,
			   'https': proxy_string % proxy}

WEB_PROXIES = {}
USER_AGENT = ''

if CONFIG_WEB not in SECTIONS:
	pprint('Web settings not found in %s' % CONFIG_FILE, 'white')
else:
	if CONFIG.has_option(CONFIG_WEB, 'proxy_host') \
		and CONFIG.has_option(CONFIG_WEB, 'proxy_port'):
		pprint('Read web proxy settings...', 'white')
		proxy = {}
		proxy['HOST'] = CONFIG.get(CONFIG_WEB, 'proxy_host')
		proxy['PORT'] = CONFIG.get(CONFIG_WEB, 'proxy_port')
		proxy_string = '%(HOST)s:%(PORT)s'
		if CONFIG.has_option(CONFIG_WEB, 'proxy_user'):
			proxy['USER'] = CONFIG.get(CONFIG_WEB, 'proxy_user')
			if CONFIG.has_option(CONFIG_WEB, 'proxy_pass'):
				proxy['PASS'] = CONFIG.get(CONFIG_WEB, 'proxy_pass')
			else:
				proxy['PASS'] = ''
			proxy_string = '%(USER)s%(PASS)s@' + proxy_string
			WEB_PROXIES = {'http':  proxy_string % proxy,
					'https': proxy_string % proxy}
	if CONFIG.has_option(CONFIG_WEB, 'user_agent'):
		USER_AGENT = CONFIG.get(CONFIG_WEB, 'user_agent')

CONFIG_API_TOKEN  = CONFIG.get(CONFIG_MAIN, 'token')
BOT_NAME          = CONFIG.get(CONFIG_MAIN, 'bot_name').lower()
PARANOIA_MODE     = get_config_bin(CONFIG, CONFIG_MAIN, 'paranoia_mode')
DEBUG_LOG         = get_config_bin(CONFIG, CONFIG_DEBUG, 'logging')
DEBUG_CONSOLE     = get_config_bin(CONFIG, CONFIG_DEBUG, 'console')
DEBUG_JSON        = get_config_bin(CONFIG, CONFIG_DEBUG, 'json')
HALT_ON_EXCEPTION = get_config_bin(CONFIG, CONFIG_DEBUG, 'halt_on_exception')
OWNER_ID          = get_config_int_array(CONFIG, CONFIG_OWNER, 'id')

API_URL = TELEGRAM_API_URL % CONFIG_API_TOKEN + '/%s'

# --- Plugins ---------------------------------------------------------------- #
pprint('*** Loading plugins', 'white')
plug_list = [p for p in os.listdir(PLUGIN_FOLDER % '') if not p.startswith('.') and p.endswith('.py')]
plug_list.sort()
COMMANDS = []
for plugin in plug_list:
	commands = []
	pprint('Append plugin: %s' % plugin, 'cyan')
	exec(open(PLUGIN_FOLDER % plugin).read())
	if commands:
		for tmp in commands:
			if len(tmp) == 5:
				tmp.append({})
			try:
				lists = CONFIG.get(CONFIG_LISTS, tmp[0]).split()
				opt = lists[0]
				if opt in ['black', 'white']:
					val = [int(v) for v in lists[1:]]
					tmp[5][opt] = val
			except:
				pass
			COMMANDS.append(tmp)
pprint('*** Total plugins: %s' % len(plug_list), 'green')
pprint('-'*50, 'blue')
pprint('Let\'s begin!', 'white')

if mode:
	try:
		send_msg(RAW_IN, 'Last mode: %s' % mode)
	except:
		pass

# --- Main cycle ------------------------------------------------------------- #

while not GAME_OVER:
	try:
		if not GAME_OVER:
			if check_updates():
				CYCLES += 1
				time.sleep(TIMEOUT)
			else:
				THREAD_ERROR_COUNT += 1
				time.sleep(MAX_TIMEOUT)
	except KeyboardInterrupt:
		pprint('Shutdown by CTRL+C...', 'bright_red')
		time.sleep(1)
		sys.exit('exit')
	except:
		MSG = '\n'.join(str(t) for t in sys.exc_info())
		pprint('*** Error *** %s ***' % MSG, 'red')
		logging.exception(' [%s] ' % timeadd(datetime.datetime.now()))
		if HALT_ON_EXCEPTION:
			raise

sys.exit(BOT_EXIT_TYPE)

# The end is near!
