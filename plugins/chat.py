#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    iSida bot VI plugin                                                      #
#    Copyright (C) Vit@liy <vitaliy@root.ua>                                  #
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

ANSW_PREV = {}
FLOOD_STATS = {}
LAST_PHRASE = {}
cur_lang = 'ru'

autophrases_time = {}
list_of_answers = {}
list_of_empty = {}
list_of_phrases_with_highlight = {}
list_of_phrases_no_highlight = {}
dict_of_mind = {}

llist = ['en', 'ru', 'ua']

for t in llist:
	chat_folder = DATA_FOLDER % 'chat/%s/' % cur_lang
	MIND_FILE = chat_folder + 'mind.txt'
	EMPTY_FILE = chat_folder + 'empty.txt'
	ANSWER_FILE = chat_folder + 'answer.txt'
	PHRASES_FILE = chat_folder + 'phrases.txt'

	list_of_answers[cur_lang] = readfile(ANSWER_FILE).split('\n')
	list_of_empty[cur_lang] = readfile(EMPTY_FILE).split('\n')
	list_of_phrases_with_highlight[cur_lang] = []
	list_of_phrases_no_highlight[cur_lang] = []
	for phrase in readfile(PHRASES_FILE).split('\n'):
		if 'NICK' in phrase:
			list_of_phrases_with_highlight[cur_lang].append(phrase)
		else:
			list_of_phrases_no_highlight[cur_lang].append(phrase)

	dict_of_mind[cur_lang] = {}
	for p in readfile(MIND_FILE).split('\n'):
		if '||' in p:
			tmp1, tmp2 = p.strip().split('||')
			dict_of_mind[cur_lang][tmp1] = tmp2.split('|')

def getSmartAnswer(ID, text):
	loc = 'ru'
	if '?' in text:
		answ = random.choice(list_of_answers[loc]).strip()
	else:
		answ = random.choice(list_of_empty[loc]).strip()
	score = 1.0
	sc = 0
	var = [answ]
	text = ' %s ' % text.upper()
	for answer in dict_of_mind[loc]:
		sc = rating(answer, text, ID)
		if sc > score:
			score = sc
			var = dict_of_mind[loc][answer]
		elif sc == score:
			var += dict_of_mind[loc][answer]

	return random.choice(var)

def rating(s, text, ID):
	r = 0.0
	s = s.split('|')
	for k in s:
		if k in text:
			r += 1
		if k in ANSW_PREV.get(ID, ''):
			r += 0.5
	return r

def getAnswer(raw_in, text):
	global ANSW_PREV
	ID = raw_in['message']['from']['id']
	text = text.strip()
	answ = getSmartAnswer(ID, text)
	ANSW_PREV[ID] = text.upper()
	return answ

# The end is near!
