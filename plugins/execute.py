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

calc_last_res = {}

def cmd_execute(raw_in, text):
	try:
		msg = html_escape_soft(remove_sub_space(str(eval(text))))
	except:
		SM = '\n'.join(str(t) for t in sys.exc_info())
		SM = html_escape_soft(SM)
		msg = 'I can\'t execute it! Error: %s' % SM
	send_msg(raw_in, '<code>%s</code>' % msg)

def cmd_calc(raw_in, text):
	global calc_last_res
	ID = raw_in['message']['from']['id']
	if 'ans' in text.lower() and calc_last_res.has_key(ID):
		text = text.lower().replace('ans', calc_last_res[ID])
	legal = string.digits + string.ascii_letters + '*/+-()=^!<>. '
	ppc = 1
	if '**' in text or 'pow' in text or 'factorial' in text:
		ppc = 0
	else:
		for tt in text:
			if tt not in legal:
				ppc = 0
				break
	if ppc:
		text = re.sub('([^.0-9]\d+)(?=([^.0-9]|$))', r'\1.0', text)
		try:
			text = remove_sub_space(str(eval(re.sub('([^a-zA-Z]|\A)([a-zA-Z])', r'\1math.\2', text))))
			if text[-2:] == '.0':
				text = text[:-2]
			calc_last_res[ID] = text
		except:
			text = 'I can\'t calculate it'
			calc_last_res[ID] = None
	else:
		text = 'Expression unacceptable!'
		calc_last_res[ID] = None
	send_msg(raw_in, text)

def cmd_dpi_calc(raw_in, text):
	text = text.strip().replace(',', '.')
	if text:
		tupl = re.findall('([0-9.]+)', text)[:3]
		if len(tupl) == 3:
			if '.' in tupl[0] or '.' in tupl[1]: msg = 'Width and height must be integer!'
			elif not float(tupl[2]): msg = 'Incorrect diagonal value!'
			else:
				dpi_type = [0, 'L'], [160, 'M'], [240, 'H'], [320, 'XH']
				dpi = int((math.sqrt(int(tupl[0])**2+int(tupl[1])**2))/float(tupl[2]))
				dpi_name = 'unknown'
				for t in dpi_type:
					if dpi > t[0]: dpi_name = '%sDPI' % t[1]
				msg = u'%s %s×%s×%s\" ➖ %sdpi [%s]' % ('📱', tupl[0], tupl[1], tupl[2], dpi, dpi_name)
		else: msg = 'Not enough parameters!'
	else: msg = 'What?'
	send_msg(raw_in, msg)

def cmd_shell(raw_in, text):
	sysshell(raw_in, text, 1)

def cms_shell_silent(raw_in, text):
	sysshell(raw_in, text, 0)

def sysshell(raw_in, text, mode):
	msg = shell_execute(text)
	if mode:
		send_msg(raw_in, msg)

commands = [['dpi', cmd_dpi_calc, False, 'less', 'DPI calculator. Width height size.'],
			['calc', cmd_calc, False, 'less', 'Calculator.'],
			['exec', cmd_execute, True, 'less', 'Execute external code.'],
			['sh', cmd_shell, True, 'all', 'Execute shell command.'],
			['shsilent', cms_shell_silent, True, 'all', 'Silent execute shell command.']]

# The end is near!
