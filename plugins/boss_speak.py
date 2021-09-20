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

def cmd_boss_speak(raw_in, text):
	raw_data = '''
		Коллеги,
		С другой стороны
		Следует, однако, всегда помнить о том, что
		При этом
		Таким образом
		Повседневная же практика показывает, что

		установленные целевые показатели
		запланированные мероприятия по подготовке кадров
		сложившиеся структуры организации
		инструменты, позволяющие контролировать весь процесс,
		ключевые показатели эффективности
		интегрированные системы отчётности

		играют важную роль в формировании
		требуют от нас анализа
		непостердственно влияют на особенности
		требуют уточнения
		обеспечивают менеджерам возможность формирования
		способствуют углубленному изучению

		оптимальных условий труда на предприятии
		возможных направлений развития в данной сфере
		практического применения разрабатываемых методик
		инфраструктурных предпосылок, с которыми мы имеем дело
		последовательной стратегии управления предприятием
		стимулов для внедрения инноваций
	'''

	if text.strip().isdigit():
		count = int(text)
		if count < 1:
			count = 1
		elif count > 36:
			count = 36
	else:
		count = 3

	msg = []
	data = [[l.strip() for l in b.split('\n') if l.strip()] for b in raw_data.strip().split('\n\n')]
	is_first = True
	while count:
		r = []
		for d in data:
			if is_first:
				f = d[0]
				is_first = False
			else:
				f = random.choice(d)
			d.remove(f)
			r.append(f)
		phrase = '%s.' % ' '.join(r)
		msg.append(phrase)
		count -= 1
		if not len(data[0]):
			data = [[l.strip() for l in b.split('\n') if l.strip()] for b in raw_data.strip().split('\n\n')]

	msg = ' '.join(msg)
	send_msg(raw_in, msg)

commands = [['boss', cmd_boss_speak, False, 'all', 'Endless boss speak.']]

# The end is near!
