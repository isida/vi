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

import os
import re
import sys
import threading
import time
import traceback

data_folder = 'data/%s'
slog_folder = data_folder % 'syslog/%s'
tmp_folder  = data_folder % 'tmp/%s'

updatelog_file  = slog_folder % 'update.log'
ver_file        = tmp_folder % 'version'
old_ver_file    = tmp_folder % 'ver'
pid_file        = tmp_folder % 'isida.pid'
starttime_file  = tmp_folder % 'starttime'

id_append = ''
GIT_VER_FORMAT    = '%s.%s-git%s'
TIME_VER_FORMAT   = '%s-none%s'
DOCKER_VER_FORMAT = '%s-docker%s'
OFFSET            = 0 # Message offset
RAW_IN            = ''
mode              = ''

def readfile(filename):
	with open(filename) as fp:
		data = fp.read()
	fp.close()
	return data

def writefile(filename, data):
	with open(filename, 'w') as fp:
		fp.write(data)
	fp.close()

def printlog(text):
	print(text)
	lt = tuple(time.localtime())
	fname = slog_folder % 'crash_%04d%02d%02d.txt' % lt[0:3]
	fbody = '%s|%s\n' % ('%02d%02d%02d' % lt[3:6],text)
	with open(fname, 'a') as fl:
		fl.write(fbody)
	fl.close()

def crashtext(t):
	t = '*** %s ***' % t
	s = '*'*len(t)
	return '\n%s\n%s\n%s\n' % (s,t,s)

def crash(text):
	printlog(crashtext(text))
	sys.exit()

def update(USED_REPO):
	if USED_REPO == 'git':
		os.system('git pull -u origin master')
		os.system('git describe --always > %s' % ver_file)
		revno = str(readfile(ver_file)).replace('\n','').replace('\r','').replace('\t','').replace(' ','')
		os.system('git log --pretty=format:'' > %s' % ver_file)
		writefile(ver_file, str(GIT_VER_FORMAT % (os.path.getsize(ver_file)+1,revno,id_append)))
		os.system('git log -1 > %s' % updatelog_file)
		writefile(updatelog_file, str(readfile(updatelog_file)).replace('\n\n','\n').replace('\r','').replace('\t',''))
	elif USED_REPO == 'docker':
		os.system('echo Update not available inside docker image! > %s' % updatelog_file)
	else:
		os.system('echo Update not available! Read wiki at http://isida.dsy.name to use GIT! > %s' % updatelog_file)

if __name__ == "__main__":
	PID = os.getpid()
	if os.name == 'nt': printlog('Warning! Correct work only on *NIX system!')

	try:
		writefile(starttime_file,str(int(time.time())))
	except:
		printlog(crashtext('Isida is crashed! Incorrent launch!'))
		raise

	if os.name != 'nt' and PID != 1 and os.path.isfile(pid_file):
		try:
			last_pid = int(readfile(pid_file))
		except:
			crash('Unable get information from %s' % pid_file)
		try:
			os.getsid(last_pid)
			crash('Multilaunch detected! Kill pid %s before launch bot again!' % last_pid)
		except:
			SM = '\n'.join(str(t) for t in sys.exc_info())
			if 'ProcessLookupError' not in SM:
				crash('Unknown exception!\n%s' % SM)

		writefile(pid_file,str(PID))

	dirs = os.listdir('.')+os.listdir('../')

	if PID == 1:
		USED_REPO = 'docker'
		writefile(ver_file, DOCKER_VER_FORMAT % (hex(int(os.path.getctime('../')))[2:], id_append))
	elif '.git' in dirs:
		USED_REPO = 'git'
		os.system('git describe --always > %s' % ver_file)
		revno = str(readfile(ver_file)).replace('\n','').replace('\r','').replace('\t','').replace(' ','')
		os.system('git log --pretty=format:'' > %s' % ver_file)
		writefile(ver_file, GIT_VER_FORMAT % (os.path.getsize(ver_file)+1,revno, id_append))
	else:
		USED_REPO = 'unknown'
		writefile(ver_file, TIME_VER_FORMAT % (hex(int(os.path.getctime('../')))[2:], id_append))

	while True:
		try:
			exec(open('kernel.py').read())
		except KeyboardInterrupt:
			break
		except SystemExit as MODE:
			for t in threading.enumerate():
				try:
					if str(t).startswith('<KThread'):
						t.kill()
					elif str(t).startswith('<_Timer'):
						t.cancel()
				except:
					pass
			mode = str(MODE)
			if mode == 'update':
				update(USED_REPO)
			elif mode == 'exit':
				break
			elif mode == 'restart':
				pass
			else:
				printlog('Unknown exit type!')
				break
		except:
			SM = '\n'.join(str(t) for t in sys.exc_info())
			printlog(crashtext('iSida is crashed! It\'s imposible, but You do it!'))
			printlog('%s\n' % SM)
			traceback.print_exc()
			break
	os._exit(0)

# The end is near!
