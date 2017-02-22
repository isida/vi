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

def cmd_domaininfo_raw(raw_in, text):
	text = text.strip().lower()
	while ' \n' in text:
		text = text.replace(' \n', '\n')
	if ''.join(re.findall(u'[-0-9a-zа-я. ]+',text,re.U+re.I)) == text and text.count('.') >= 1 and len(text) > 4:
		if text.startswith('sites '):
			t = 2
			text = text.split(' ')[1]
			regex = '<h3>(.*?)<br></font><br><br>'
		else:
			t = 1
			regex = '</a><br /><h3>(.*?)<br /></font></blockquote>'
		url = 'http://1whois.ru/index.php?url=%s&t=%s' % (text.encode('idna'), t)
		body = deidna(html_encode(load_page(url).replace('&nbsp;', ' ')))
		try:
			body = re.findall(regex, body, re.S)
			if body:
				msg = unhtml_hard(''.join(body[0]))
			else:
				msg = 'No data!'
		except:
			msg = 'Unexpected error'
	else:
		msg = 'Error!'
	send_msg(raw_in,msg)

def cmd_domaininfo(raw_in, text):
	text = text.strip().lower()
	while ' \n' in text:
		text = text.replace(' \n','\n')
	if ''.join(re.findall(u'[-0-9a-zа-я. ]+',text,re.U+re.I)) == text and text.count('.') >= 1 and len(text) > 4:
		if 'sites' in text:
			t = 2
			text = text.split(' ')[1]
			regex = '<font color="black" size="2">(.*?)</font>'
			msg = 'Sites at Domain/IP address: %s' % text
		else:
			t = 1
			regex = '<blockquote><font.*?>(.*?)</font></blockquote>'
			msg = 'Domain/IP address info:'
		url = 'http://1whois.ru/index.php?url=%s&t=%s' % (text.encode('idna'),t)
		body = deidna(html_encode(load_page(url).replace('&nbsp;', ' ')))
		try:
			body = re.findall(regex, body, re.S)[0]
			if u'Нет данных!' in body:
				msg += ' ' + 'No data!'
			else:
				tmp_body = {}
				body = replacer(body).split('\n')
				newbody = []
				for tmp in body:
					if ':' in tmp:
						if len(tmp.split(':')[0].split()) <= 2 and len(tmp.split(':')[1]) >= 2:
							if not tmp_body.has_key(tmp.split(':')[1]):
								tmp_body[tmp.split(':')[1]]=tmp.split(':')[0]
								newbody.append(tmp)
					elif tmp.count(' ') <= 4 and not tmp_body.has_key(tmp):
						tmp_body[tmp] = tmp
						newbody.append(tmp)
				msg += '\n'+'\n'.join(newbody)
		except:
			raise
			#msg = 'Unexpected error'
	else:
		msg = 'Error!'
	send_msg(raw_in,msg)

commands = [['domain_info', cmd_domaininfo, False, 'less', 'Domain/IP address whois info.'],
			['domain_info_raw', cmd_domaininfo_raw, False, 'less', 'Domain/IP address whois info.']]

# The end is near!
