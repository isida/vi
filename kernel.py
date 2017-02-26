#!/usr/bin/python
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
import ConfigParser
import json
import logging
import math
import os
import requests
import time
import urllib
import urllib2
import random
import re
import socket
import string
import sys
import threading

# Reload sys for apply UTF-8 encoding
reload(sys)
sys.setdefaultencoding('UTF8')

# Threads with `kill` function
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
def thr(func,param,name):
	global THREAD_COUNT, THREAD_ERROR_COUNT, sema
	THREAD_COUNT += 1
	try:
		tmp_th = KThread(group=None,target=log_execute,name='%s_%s' % \
						(THREAD_COUNT,name),args=(func,param))
		tmp_th.start()
	except SystemExit:
		pass
	except Exception, MSG:
		try:
			MSG = str(MSG)
		except:
			MSG = unicode(MSG)
		if 'thread' in MSG.lower():
			THREAD_ERROR_COUNT += 1
		else:
			logging.exception(' [%s] %s' % (timeadd(tuple(time.localtime())), \
								unicode(func)))
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
		logging.exception(' [%s] %s' % (timeadd(tuple(time.localtime())), \
							unicode(proc)))

# Decode from IDNA
def deidna(text):
	def repl(t):
		return t.group().lower().decode('idna')
	return re.sub(r'(xn--[-0-9a-z_]*)',repl,text,flags=re.S|re.I|re.U)

# Encode to IDNA
def enidna(text):
	idn = re.findall(u'http[s]?://([-0-9a-zа-я._]*)',text,flags=re.S|re.I|re.U)
	if idn:
		text = text.replace(idn[0],idn[0].lower().encode('idna'))
	return text.encode('utf-8')

# RAW-Encode to IDNA
def enidna_raw(text):
	def repl(t):
		return t.group().lower().encode('idna')
	return re.sub(u'([а-я][-0-9а-я_]*)',repl,text,flags=re.S|re.I|re.U)

# Detect HTML encoding and encode it
def html_encode(body):
	encidx = re.findall('encoding=["\'&]*(.*?)["\'& ]{1}',body[:1024])
	if encidx:
		enc = encidx[0]
	else:
		encidx = re.findall('charset=["\'&]*(.*?)["\'& ]{1}',body[:1024])
		if encidx: enc = encidx[0]
		else: enc = chardet.detect(body)['encoding']
	if body == None:
		body = ''
	if enc == None or enc == '' or enc.lower() == 'unicode':
		enc = 'utf-8'
	if enc == 'ISO-8859-2':
		tx,splitter = '','|'
		while splitter in body:
			splitter += '|'
		tbody = body.replace('</','<'+splitter+'/').split(splitter)
		cntr = 0
		for tmp in tbody:
			try:
				enc = chardet.detect(tmp)['encoding']
				if enc == None or enc == '' or enc.lower() == 'unicode':
					enc = 'utf-8'
				tx += unicode(tmp,enc)
			except:
				ttext = ''
				for tmp2 in tmp:
					if (tmp2<='~'):
						ttext += tmp2
					else:
						ttext += '?'
				tx += ttext
			cntr += 1
		return tx
	else:
		try:
			return smart_encode(body,enc)
		except:
			return 'Encoding error!'

# Encode HTML with mixed encoding
def smart_encode(text,enc):
	tx = ''
	splitter = '|'
	while splitter in text:
		splitter += '|'
	ttext = text.replace('</','<%s/' % splitter).split(splitter)
	for tmp in ttext:
		try:
			tx += unicode(tmp,enc)
		except:
			pass
	return tx

# Soft escape html
def html_escape_soft(text):
	for tmp in (('<','&lt;'),('>','&gt;')):
		text = text.replace(tmp[0], tmp[1])
	return text

# Read file
def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

# Write file
def writefile(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()

# Get file or get default data
def getFile(filename,default):
	if os.path.isfile(filename):
		try:
			filebody = eval(readfile(filename))
		except:
			if os.path.isfile(back_file % filename.split('/')[-1]):
				while True:
					try:
						filebody = eval(readfile(back_file % \
										filename.split('/')[-1]))
						break
					except:
						pass
			else:
				filebody = default
				writefile(filename,str(default))
	else:
		filebody = default
		writefile(filename,str(default))
	writefile(back_file % filename.split('/')[-1],str(filebody))
	return filebody

def replace_ltgt(text):
	return remove_replace_ltgt(text,' ')

def remove_replace_ltgt(text,item):
	T = re.findall('<.*?>', text, re.S)
	for tmp in T:
		text = text.replace(tmp,item,1)
	return text

def rss_replace(ms):
	for tmp in lmass:
		ms = ms.replace(tmp[1],tmp[0])
	return unescape(esc_min(ms))

def esc_min(ms):
	for tmp in rmass:
		ms = ms.replace(tmp[1],tmp[0])
	return ms

def unescape(text):
	def fixup(m):
		text = m.group(0)
		if text[:2] == '&#':
			try:
				if text[:3] == '&#x':
					return unichr(int(text[3:-1], 16))
				else:
					return unichr(int(text[2:-1]))
			except ValueError:
				pass
		else:
			try:
				text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
			except KeyError:
				pass
		return text
	return re.sub('&#?\w+;', fixup, text)

# Hard remove HTML tags
def unhtml_raw(page,mode):
	for a in range(0,page.count('<style')):
		ttag = get_tag_full(page,'style')
		page = page.replace(ttag,'')

	for a in range(0,page.count('<script')):
		ttag = get_tag_full(page,'script')
		page = page.replace(ttag,'')

	page = rss_replace(page)
	if mode:
		page = replace_ltgt(page)
	else:
		page = rss_repl_html(page)
	page = rss_replace(page)
	page = rss_del_nn(page)
	page = page.replace('\n ','')
	return page

def rss_del_nn(ms):
	ms = ms.replace('\r',' ').replace('\t',' ')
	while '\n ' in ms:
		ms = ms.replace('\n ','\n')
	while len(ms) and (ms[0] == '\n' or ms[0] == ' '):
		ms = ms[1:]
	while '\n\n' in ms:
		ms = ms.replace('\n\n','\n')
	while '  ' in ms:
		ms = ms.replace('  ',' ')
	while u'\n\n•' in ms:
		ms = ms.replace(u'\n\n•',u'\n•')
	while u'• \n' in ms:
		ms = ms.replace(u'• \n',u'• ')
	return ms.strip()

def unhtml(page):
	return unhtml_raw(page,None)

def unhtml_hard(page):
	return unhtml_raw(page,True)

# Get Bot's version
def get_bot_version():
	if os.path.isfile(ver_file):
		bvers = readfile(ver_file).decode('utf-8').replace('\n','').\
					replace('\r','').replace('\t','').replace(' ','')
		bV = '%s.%s-%s' % (botVersionDef,bvers,base_type)
	else:
		bV = '%s-%s' % (botVersionDef, base_type)
	return bV

# Get OS version
def get_os_version():
	iSys = sys.platform
	iOs = os.name
	isidaPyVer = '%s [%s]' % (sys.version.split(' (')[0],sys.version.split(')')[0].split(', ')[1])
	if iOs == 'posix':
		osInfo = os.uname()
		isidaOs = '%s %s-%s / Python %s' % (osInfo[0],osInfo[2],osInfo[4],isidaPyVer)
	elif iSys == 'win32':
		def get_registry_value(key, subkey, value):
			import _winreg
			key = getattr(_winreg, key)
			handle = _winreg.OpenKey(key, subkey)
			(value, type) = _winreg.QueryValueEx(handle, value)
			return value
		def get(key):
			return get_registry_value("HKEY_LOCAL_MACHINE", "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",key)
		osInfo = ' '.join(get("ProductName").split()[:3])
		buildInfo = get("CurrentBuildNumber")
		try:
			spInfo = get("CSDVersion")
			isidaOs = '%s %s [%s] / Python %s' % (osInfo,spInfo,buildInfo,isidaPyVer)
		except:
			isidaOs = '%s [%s] / Python %s' % (osInfo,buildInfo,isidaPyVer)
	else:
		isidaOs = 'unknown'
	return isidaOs
	
# Get color by name on Linux
def get_color(c):
	color = os.environ.has_key('TERM')
	colors = {'clear':'[0m','blue':'[34m','red':'[31m','magenta':'[35m',
			  'green':'[32m','cyan':'[36m','brown':'[33m','light_gray':'[37m',
			  'black':'[30m','bright_blue':'[34;1m','bright_red':'[31;1m',
			  'purple':'[35;1m','bright_green':'[32;1m','bright_cyan':'[36;1m',
			  'yellow':'[33;1m','dark_gray':'[30;1m','white':'[37;1m'}
	return ['','\x1b%s' % colors[c]][color]

# Get color by name on Windows
def get_color_win32(c):
	colors = {'clear':7,'blue':1,'red':4,'magenta':5,'green':2,'cyan':3,
			  'brown':6,'light_gray':7,'black':0,'bright_blue':9,
			  'bright_red':12,'purple':13,'bright_green':10,'bright_cyan':11,
			  'yellow':14,'dark_gray':8,'white':15}
	return colors[c]

# Time and date to string
def timeadd(lt):
	return '%04d.%02d.%02d %02d:%02d:%02d' % lt[0:6]

# Time to string
def onlytimeadd(lt):
	return '%02d:%02d:%02d' % lt[3:6]

# Exclude non-ascii symbols
def parser(t):
	try:
		return ''.join([['?',l][l<='~'] for l in unicode(t)])
	except:
		fp = file(slog_folder % 'critical_exception_%s.txt' % int(time.time()), 'wb')
		fp.write(t)
		fp.close()

# Log message
def pprint(*text):
	global last_logs_store
	c,wc,win_color = '','',''
	if len(text) > 1:
		if is_win32:
			win_color = get_color_win32(text[1])
		else:
			c,wc = get_color(text[1]),get_color('clear')
	elif is_win32:
		win_color = get_color_win32('clear')
	text = text[0]
	lt = tuple(time.localtime())
	zz = '%s[%s]%s %s%s' % (wc,onlytimeadd(lt),c,text,wc)
	last_logs_store = ['[%s] %s' % (onlytimeadd(lt),text)] + \
						last_logs_store[:last_logs_size]
	if DEBUG_CONSOLE:
		if is_win32 and win_color:
			ctypes.windll.Kernel32.SetConsoleTextAttribute(win_console_color, \
				get_color_win32('clear'))
			print zz.split(' ',1)[0],
			ctypes.windll.Kernel32.SetConsoleTextAttribute(win_console_color, \
				win_color)
			try:
				print zz.split(' ',1)[1]
			except:
				print parser(zz.split(' ',1)[1])
			ctypes.windll.Kernel32.SetConsoleTextAttribute(win_console_color, \
				get_color_win32('clear'))
		else:
			try:
				print zz
			except:
				print parser(zz)
	if DEBUG_LOG:
		fname = SYSLOG_FOLDER % '%02d%02d%02d.txt' % lt[0:3]
		fbody = '%s|%s\n' % (onlytimeadd(lt),text.replace('\n','\r'))
		fl = open(fname, 'a')
		fl.write(fbody.encode('utf-8'))
		fl.close()

# Error message
def Error(text):
	print 'Error! %s' % text
	sys.exit()

# Get integer value from config
def get_config_int(_config, _section, _name):
	try:
		return int(_config.get(_section, _name))
	except:
		return -1

# Get binary value from config
# True == 1, '1', 'yes', 'true'
# False == all else
def get_config_bin(_config, _section, _name):
	try:
		_var = int(_config.get(_section, _name))
	except:
		_var = _config.get(_section, _name).lower()
	_True = [1, '1', 'yes', 'true']
	if _var in _True:
		return True
	else:
		return False

# Replace non-ascii and TAB, CR, LF
def remove_sub_space(t):
	return ''.join([['?',l][l>=' ' or l in '\t\r\n'] for l in unicode(t)])

# Send message
def send_msg(raw_in, msg, parse_mode = 'HTML', custom = None):
	global LAST_MESSAGE, TIMEOUT
	#if parse_mode == 'HTML':
	#	msg = html_escape_soft(msg)
	MSG = { 'chat_id': raw_in['message']['chat'].get('id',''),
			'text': msg,
			'parse_mode': parse_mode }
	if custom:
		for t in custom.keys():
			MSG[t] = custom[t]
	request = requests.post(API_URL % 'sendMessage', data=MSG)
	LAST_MESSAGE = time.time()
	TIMEOUT = MIN_TIMEOUT
	if not request.status_code == 200:
		pprint('*** Error code on sendMessage: %s' % request.status_code, 'red')
		pprint('Raw_in dump:\n%s' % json.dumps(raw_in, indent=2, separators=(',', ': ')), 'red')
		pprint('Data dump:\n%s' % json.dumps(MSG, indent=2, separators=(',', ': ')), 'red')
		return False
	else:
		return True

# Open web page
def get_opener(page_name, parameters=None):
	socket.setdefaulttimeout(www_get_timeout)
	try:
		proxy_support = urllib2.ProxyHandler({'http' : \
			'http://%(user)s:%(password)s@%(host)s:%(port)d' % http_proxy})
		opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
		urllib2.install_opener(opener)
	except:
		opener = urllib2.build_opener(urllib2.HTTPHandler)
	opener.addheaders = [('User-agent', user_agent)]
	if parameters:
		page_name += urllib.urlencode(parameters)
	try:
		data = opener.open(page_name)
		result = True
	except Exception, MSG:
		try:
			MSG = str(MSG)
		except:
			MSG = unicode(MSG)
		data = 'Error! %s' % MSG.replace('>','').replace('<','').capitalize()
		result = False
	return data, result

# Load page with limited size
def load_page_size(page_name, page_size, parameters=None):
	data, result = get_opener(page_name, parameters)
	if result:
		return data.read(page_size)
	else:
		return data

# Load page without limited size
def load_page(page_name, parameters=None):
	data, result = get_opener(page_name, parameters)
	if result:
		return data.read(size_overflow)
	else:
		return data

# Check new incoming messages
def check_updates():
	global OFFSET
	data = {'limit': 0,
			'timeout': 0}
	if OFFSET:
		data['offset'] = OFFSET + 1

	try:
		request = requests.post(API_URL % 'getUpdates', data=data)
	except requests.exceptions.ConnectionError:
		pprint('*** Connection error on getUpdates. Waiting %s seconds.' % MAX_TIMEOUT, 'red')
		time.sleep(MAX_TIMEOUT)
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
		OFFSET = msg_in['update_id']
		if msg_in.has_key('edited_message'):
			msg_in['message'] = msg_in['edited_message']
			pprint('*** Edited message!', 'yellow')

		#send_msg(msg_in, '<i>Edited messages not supported now!</i>')

		if 'message' not in msg_in or 'text' not in msg_in['message']:
			if msg_in['message'].has_key('new_chat_participant'):
				pprint('New participant|%s' % '|'.join([str(t) for t in [\
					msg_in['message']['chat'].get('all_members_are_administrators',''), \
					msg_in['message']['chat'].get('type',''), \
					msg_in['message']['chat'].get('id',''), \
					msg_in['message']['chat'].get('title',''), \
					msg_in['message']['new_chat_participant'].get('id',''), \
					msg_in['message']['new_chat_participant'].get('username',''), \
					msg_in['message']['new_chat_participant'].get('first_name',''), \
					msg_in['message']['new_chat_participant'].get('last_name','') ]]),'cyan')
				break
			elif msg_in['message'].has_key('left_chat_participant'):
				pprint('Left participant|%s' % '|'.join([str(t) for t in [\
					msg_in['message']['chat'].get('all_members_are_administrators',''), \
					msg_in['message']['chat'].get('type',''), \
					msg_in['message']['chat'].get('id',''), \
					msg_in['message']['chat'].get('title',''), \
					msg_in['message']['left_chat_participant'].get('id',''), \
					msg_in['message']['left_chat_participant'].get('username',''), \
					msg_in['message']['left_chat_participant'].get('first_name',''), \
					msg_in['message']['left_chat_participant'].get('last_name','') ]]),'cyan')
				break
			else:
				pprint('Unknown message', 'red')
				pprint(json.dumps(msg_in, indent=2, separators=(',', ': ')), 'magenta')
				continue

		IS_OWNER = msg_in['message']['from'].get('id', '') == OWNER_ID
		CMD = msg_in['message'].get('text','').strip()
		_ID = msg_in['message']['from'].get('id','')
		_USERNAME = msg_in['message']['from'].get('username','')
		_FIRST_NAME = msg_in['message']['from'].get('first_name','')
		_LAST_NAME = msg_in['message']['from'].get('last_name','')

		pprint('|'.join([str(t) for t in [_ID, _USERNAME, _FIRST_NAME, \
			_LAST_NAME, CMD]]),'cyan')
		# name, proc, is_owner, data_type
		#commands = ['whoami', cmd_whoami, False, 'raw']
		# Command parser!
		IS_COMMAND = False
		for c in COMMANDS:
			if c[2] and IS_OWNER:
				ALLOW = True
			elif not c[2]:
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
						thr(c[1], (msg_in,), CMD)
					elif c[3] in ['less', 'all']:
						less = CMD[len(c[0]):].strip()
						if less.lower().startswith('@%s' % BOT_NAME):
							less = less[len(BOT_NAME)+1:].strip()
						if c[3] == 'less' and not less:
							send_msg(msg_in,'⚠️ Required parametr missed!')
						else:
							thr(c[1], (msg_in, less), CMD)
				else:
					send_msg(msg_in,'🔒 Locked! Command allowed only for bot\'s owner.')
				IS_COMMAND = True
				break

		if not IS_COMMAND:
			if (msg_in['message']['text'].lower().startswith('@%s ' % BOT_NAME) and \
					msg_in['message'].has_key('chat') and \
					msg_in['message']['chat'].has_key('type') and \
					msg_in['message']['chat'].get('type','') in ['group', 'supergroup']) or \
					(msg_in['message'].has_key('reply_to_message') and \
					msg_in['message']['reply_to_message'].has_key('from') and \
					msg_in['message']['reply_to_message']['from'].has_key('username') and \
					msg_in['message']['reply_to_message']['from'].get('username','').lower() == BOT_NAME):
				text = msg_in['message']['text']
				if text.lower().startswith('@%s ' % BOT_NAME):
					text = text[len(BOT_NAME)+1:].strip()
				pprint('>>> Chat: %s' % text, 'green')
				msg = getAnswer(msg_in, text)
				pprint('<<< Chat: %s' % msg, 'bright_green')
				send_msg(msg_in, msg)
			elif (msg_in['message'].has_key('chat') and \
					msg_in['message']['chat'].has_key('type') and \
					msg_in['message']['chat'].get('type','') == 'private'):
				text = msg_in['message'].get('text').strip()
				pprint('>>> Chat: %s' % text, 'green')
				msg = getAnswer(msg_in, text)
				pprint('<<< Chat: %s' % msg, 'bright_green')
				send_msg(msg_in, msg)
			else:
				pass
				#pprint('Unknown message', 'red')
				#pprint(json.dumps(msg_in, indent=2, separators=(',', ': ')), 'magenta')

def get_tag(body,tag):
	T = re.findall('<%s.*?>(.*?)</%s>' % (tag,tag),body,re.S)
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
			error_answ = os.system('%s > %s 2>&1' % (cmd.encode('utf-8'),tmp_file))
			if not error_answ:
				try:
					body = html_escape_soft(readfile(tmp_file))
				except:
					body = '⚠️ Command execution error.'
				if len(body):
					enc = chardet.detect(body)['encoding']
					result = remove_sub_space(unicode(body,enc))
				else:
					result = 'ok'
			else:
				result = '⚠️ Command execution error.'
				try:
					result += '\n' + html_escape_soft(readfile(tmp_file))
				except:
					pass
		except Exception, MSG:
			try:
				MSG = str(MSG)
			except:
				MSG = unicode(MSG)
			result = '⚠️ I can\'t execute it! Error: %s' % MSG
		try:
			os.remove(tmp_file)
		except:
			pass
	return '<code>%s</code>' % result

# --- Let's begin! -------------------------------------------------------------- #
lmass = (('\n','<br>'),('\n','<br />'),('\n','<br/>'),('\n','\n\r'),
		('','<![CDATA['),('',']]>'),('','&shy;'),('','&ensp;'),('','&emsp;'),
		('','&thinsp;'),('','&zwnj;'),('','&zwj;'))
rmass = (('&','&amp;'),('\"','&quot;'),('\'','&apos;'),('~','&tilde;'),
		(' ','&nbsp;'),('<','&lt;'),('>','&gt;'),(u'¡','&iexcl;'),
		(u'¢','&cent;'),(u'£','&pound;'),(u'¤','&curren;'),(u'¥','&yen;'),
		(u'¦','&brvbar;'),(u'§','&sect;'),(u'¨','&uml;'),(u'©','&copy;'),
		(u'ª','&ordf;'),(u'«','&laquo;'),(u'¬','&not;'),(u'®','&reg;'),
		(u'¯','&macr;'),(u'°','&deg;'),(u'±','&plusmn;'),(u'²','&sup2;'),
		(u'³','&sup3;'),(u'´','&acute;'),(u'µ','&micro;'),(u'¶','&para;'),
		(u'·','&middot;'),(u'¸','&cedil;'),(u'¹','&sup1;'),(u'º','&ordm;'),
		(u'»','&raquo;'),(u'¼','&frac14;'),(u'½','&frac12;'),(u'¾','&frac34;'),
		(u'¿','&iquest;'),(u'×','&times;'),(u'÷','&divide;'),(u'À','&Agrave;'),
		(u'Á','&Aacute;'),(u'Â','&Acirc;'),(u'Ã','&Atilde;'),(u'Ä','&Auml;'),
		(u'Å','&Aring;'),(u'Æ','&AElig;'),(u'Ç','&Ccedil;'),(u'È','&Egrave;'),
		(u'É','&Eacute;'),(u'Ê','&Ecirc;'),(u'Ë','&Euml;'),(u'Ì','&Igrave;'),
		(u'Í','&Iacute;'),(u'Î','&Icirc;'),(u'Ï','&Iuml;'),(u'Ð','&ETH;'),
		(u'Ñ','&Ntilde;'),(u'Ò','&Ograve;'),(u'Ó','&Oacute;'),(u'Ô','&Ocirc;'),
		(u'Õ','&Otilde;'),(u'Ö','&Ouml;'),(u'Ø','&Oslash;'),(u'Ù','&Ugrave;'),
		(u'Ú','&Uacute;'),(u'Û','&Ucirc;'),(u'Ü','&Uuml;'),(u'Ý','&Yacute;'),
		(u'Þ','&THORN;'),(u'ß','&szlig;'),(u'à','&agrave;'),(u'á','&aacute;'),
		(u'â','&acirc;'),(u'ã','&atilde;'),(u'ä','&auml;'),(u'å','&aring;'),
		(u'æ','&aelig;'),(u'ç','&ccedil;'),(u'è','&egrave;'),(u'é','&eacute;'),
		(u'ê','&ecirc;'),(u'ë','&euml;'),(u'ì','&igrave;'),(u'í','&iacute;'),
		(u'î','&icirc;'),(u'ï','&iuml;'),(u'ð','&eth;'),(u'ñ','&ntilde;'),
		(u'ò','&ograve;'),(u'ó','&oacute;'),(u'ô','&ocirc;'),(u'õ','&otilde;'),
		(u'ö','&ouml;'),(u'ø','&oslash;'),(u'ù','&ugrave;'),(u'ú','&uacute;'),
		(u'û','&ucirc;'),(u'ü','&uuml;'),(u'ý','&yacute;'),(u'þ','&thorn;'),
		(u'ÿ','&yuml;'),(u'∀','&forall;'),(u'∂','&part;'),(u'∃','&exists;'),
		(u'∅','&empty;'),(u'∇','&nabla;'),(u'∈','&isin;'),(u'∉','&notin;'),
		(u'∋','&ni;'),(u'∏','&prod;'),(u'∑','&sum;'),(u'−','&minus;'),
		(u'∗','&lowast;'),(u'√','&radic;'),(u'∝','&prop;'),(u'∞','&infin;'),
		(u'∠','&ang;'),(u'∧','&and;'),(u'∨','&or;'),(u'∩','&cap;'),
		(u'∪','&cup;'),(u'∫','&int;'),(u'∴','&there4;'),(u'∼','&sim;'),
		(u'≅','&cong;'),(u'≈','&asymp;'),(u'≠','&ne;'),(u'≡','&equiv;'),
		(u'≤','&le;'),(u'≥','&ge;'),(u'⊂','&sub;'),(u'⊃','&sup;'),
		(u'⊄','&nsub;'),(u'⊆','&sube;'),(u'⊇','&supe;'),(u'⊕','&oplus;'),
		(u'⊗','&otimes;'),(u'⊥','&perp;'),(u'⋅','&sdot;'),(u'Α','&Alpha;'),
		(u'Β','&Beta;'),(u'Γ','&Gamma;'),(u'Δ','&Delta;'),(u'Ε','&Epsilon;'),
		(u'Ζ','&Zeta;'),(u'Η','&Eta;'),(u'Θ','&Theta;'),(u'Ι','&Iota;'),
		(u'Κ','&Kappa;'),(u'Λ','&Lambda;'),(u'Μ','&Mu;'),(u'Ν','&Nu;'),
		(u'Ξ','&Xi;'),(u'Ο','&Omicron;'),(u'Π','&Pi;'),(u'Ρ','&Rho;'),
		(u'Σ','&Sigma;'),(u'Τ','&Tau;'),(u'Υ','&Upsilon;'),(u'Φ','&Phi;'),
		(u'Χ','&Chi;'),(u'Ψ','&Psi;'),(u'Ω','&Omega;'),(u'α','&alpha;'),
		(u'β','&beta;'),(u'γ','&gamma;'),(u'δ','&delta;'),(u'ε','&epsilon;'),
		(u'ζ','&zeta;'),(u'η','&eta;'),(u'θ','&theta;'),(u'ι','&iota;'),
		(u'κ','&kappa;'),(u'λ','&lambda;'),(u'μ','&mu;'),(u'ν','&nu;'),
		(u'ξ','&xi;'),(u'ο','&omicron;'),(u'π','&pi;'),(u'ρ','&rho;'),
		(u'ς','&sigmaf;'),(u'σ','&sigma;'),(u'τ','&tau;'),(u'υ','&upsilon;'),
		(u'φ','&phi;'),(u'χ','&chi;'),(u'ψ','&psi;'),(u'ω','&omega;'),
		(u'ϑ','&thetasym;'),(u'ϒ','&upsih;'),(u'ϖ','&piv;'),(u'Œ','&OElig;'),
		(u'œ','&oelig;'),(u'Š','&Scaron;'),(u'š','&scaron;'),(u'Ÿ','&Yuml;'),
		(u'ƒ','&fnof;'),(u'ˆ','&circ;'),(u'‎','&lrm;'),(u'‏','&rlm;'),
		(u'–','&ndash;'),(u'—','&mdash;'),(u'‘','&lsquo;'),(u'’','&rsquo;'),
		(u'‚','&sbquo;'),(u'“','&ldquo;'),(u'”','&rdquo;'),(u'„','&bdquo;'),
		(u'†','&dagger;'),(u'‡','&Dagger;'),(u'•','&bull;'),(u'…','&hellip;'),
		(u'‰','&permil;'),(u'′','&prime;'),(u'″','&Prime;'),(u'‹','&lsaquo;'),
		(u'›','&rsaquo;'),(u'‾','&oline;'),(u'€','&euro;'),(u'™','&trade;'),
		(u'←','&larr;'),(u'↑','&uarr;'),(u'→','&rarr;'),(u'↓','&darr;'),
		(u'↔','&harr;'),(u'↵','&crarr;'),(u'⌈','&lceil;'),(u'⌉','&rceil;'),
		(u'⌊','&lfloor;'),(u'⌋','&rfloor'),(u'◊','&loz;'),(u'♠','&spades;'),
		(u'♣','&clubs;'),(u'♥','&hearts;'),(u'♦','&diams;'))
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
botName            = 'iSida'                          # Bot's name
botVersionDef      = '6.0'                            # Bot's version
base_type          = 'NoDB'                           # Bot's base type
www_get_timeout    = 15                               # Timeout for web requests
size_overflow      = 262144                           # Web page limit in bytes
#http_proxy         = {'host':'127.0.0.1','port':3128,'user':None,'password':None}
#                                                     # Proxy settings
user_agent         = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
#                                                     # User agent for web requests
MIN_TIMEOUT        = 1                                # Minimal timeout between request updates
MAX_TIMEOUT        = 15                               # Maximal timeout between request updates
TIMEOUT            = 1                                # Default timeout between request updates
LAST_MESSAGE       = time.time()                      # Last message time
TIMEOUT_DIFF       = 60                               # Little sleep every 60 seconds
TIMEOUT_STEP       = 1.3                              # Size of update time sleep
CYCLES             = 0                                # Work cycles
THREAD_COUNT       = 0                                # Executed threads
THREAD_ERROR_COUNT = 0                                # Threads with error
GAME_OVER          = False                            # Bot's status
BOT_EXIT_TYPE      = ''                               # Reason for bot's kernel exit

# --- Init ------------------------------------------------------------------- #
try:
	_ = OFFSET
except NameError:
	OFFSET = 0
logging.basicConfig(filename=LOG_FILENAME)#,level=logging.DEBUG,)
sema = threading.BoundedSemaphore(value=30)
is_win32 = sys.platform == 'win32'
if is_win32:
	import ctypes
	ctypes.windll.Kernel32.GetStdHandle.restype = ctypes.c_ulong
	win_console_color = ctypes.windll.Kernel32.GetStdHandle(ctypes.c_ulong(0xfffffff5))

pprint('-'*50,'blue')
pprint('%s %s // %s' % (botName, get_bot_version(), get_os_version()), 'bright_cyan')
pprint('-'*50,'blue')
pprint('*** Init enviroment succed', 'white')

# --- Config ----------------------------------------------------------------- #
pprint('*** Loadnig config', 'white')
if not os.path.exists(CONFIG_FILE):
	Error('Config file not found: %s' % CONFIG_FILE)
CONFIG = ConfigParser.ConfigParser()
CONFIG.read(CONFIG_FILE)
SECTIONS = CONFIG.sections()
if CONFIG_MAIN not in SECTIONS:
	Error('Main options not found in %s' % CONFIG_FILE)
if CONFIG_DEBUG not in SECTIONS:
	Error('Debug options not found in %s' % CONFIG_FILE)
if CONFIG_OWNER not in SECTIONS:
	Error('Owner options not found in %s' % CONFIG_FILE)

CONFIG_API_TOKEN  = CONFIG.get(CONFIG_MAIN,'token')
BOT_NAME          = CONFIG.get(CONFIG_MAIN,'bot_name').lower()
PARANOIA_MODE     = get_config_bin(CONFIG, CONFIG_MAIN, 'paranoia_mode')
DEBUG_LOG         = get_config_bin(CONFIG, CONFIG_DEBUG, 'logging')
DEBUG_CONSOLE     = get_config_bin(CONFIG, CONFIG_DEBUG, 'console')
DEBUG_JSON        = get_config_bin(CONFIG, CONFIG_DEBUG, 'json')
HALT_ON_EXCEPTION = get_config_bin(CONFIG, CONFIG_DEBUG, 'halt_on_exception')
OWNER_ID          = get_config_int(CONFIG, CONFIG_OWNER, 'id')
try:
	MAX_TIMEOUT   = get_config_bin(CONFIG, CONFIG_OWNER, 'max_timeout')
except:
	pass

API_URL = TELEGRAM_API_URL % CONFIG_API_TOKEN + '/%s'

# --- Plugins ---------------------------------------------------------------- #
pprint('*** Loading plugins', 'white')
plug_list = [p for p in os.listdir(PLUGIN_FOLDER % '') if not p.startswith('.') and p.endswith('.py')]
plug_list.sort()
COMMANDS = []
for plugin in plug_list:
	commands = []
	pprint('Append plugin: %s' % plugin, 'cyan')
	execfile(PLUGIN_FOLDER % plugin)
	if commands:
		for tmp in commands:
			COMMANDS.append(tmp)
pprint('*** Total plugins: %s' % len(plug_list),'green')
pprint('-'*50,'blue')
pprint('Let\'s begin!','white')

# --- Main cycle ------------------------------------------------------------- #
while not GAME_OVER:
	try:
		check_updates()
		if (time.time() - LAST_MESSAGE) > TIMEOUT_DIFF and TIMEOUT <= MAX_TIMEOUT:
			TIMEOUT = TIMEOUT * TIMEOUT_STEP
			LAST_MESSAGE = time.time()
			pprint('*** Sleep time: %.02f' % TIMEOUT, 'brown')
		CYCLES += 1
		time.sleep(TIMEOUT)
	except KeyboardInterrupt:
		pprint('Shutdown by CTRL+C...','bright_red')
		time.sleep(1)
		sys.exit('exit')
	except Exception, MSG:
		try:
			MSG = str(MSG)
		except:
			MSG = unicode(MSG)
		pprint('*** Error *** %s ***' % MSG, 'red')
		logging.exception(' [%s] ' % timeadd(tuple(time.localtime())))
		if HALT_ON_EXCEPTION:
			raise

sys.exit(BOT_EXIT_TYPE)

# The end is near!
