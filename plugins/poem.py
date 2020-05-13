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

def cmd_poem(raw_in):
	dict = [['Я помню', 'Не помню', 'Забыть бы', 'Купите', 'Очкуешь', 'Какое', \
				'Угробил', 'Открою', 'Ты чуешь?'],
			['чудное', 'странное', 'некое', 'вкусное', 'пьяное', 'свинское', \
				'чоткое', 'сраное', 'нужное', 'конское'],
			['мгновенье,', 'затменье,', 'хотенье,', 'варенье,', 'творенье,', \
				'везенье,', 'рожденье,', 'смущенье,', 'печенье,', 'ученье,'],
			['\n'],
			['Передомной', 'Под косячком', 'На кладбище', 'В моих мечтах', 'Под скальпилем', \
				'В моих штанах', 'Из-за угла', 'В моих ушах', 'В ночном горшке', 'Из головы',],
			['явилась ты,', 'добилась ты,', 'торчат кресты,', 'стихов листы,', 'забилась ты,', \
				'мои трусы,', 'поют дрозды,', 'из темноты,', 'помылась ты,', 'дают пизды,'],
			['\n'],
			['Как'],
			['мимолётное', 'детородное', 'психотропное', 'кайфоломное', 'очевидное', \
				'у воробушков', 'эдакое вот', 'нам не чуждое', 'благородное', 'ябывдульское'],
			['виденье,', 'сиденье,', 'паренье,', 'сужденье,', 'вращенье,', 'сношенье,', \
				'смятенье,', 'теченье,', 'паденье,', 'сплетенье,'],
			['\n'],
			['Как'],
			['гений', 'сторож', 'символ', 'спарта', 'правда', 'ангел', \
				'водка', 'пиво', 'ахтунг', 'жопа'],
			['чистой', 'вечной', 'тухлой', 'просит', 'грязной', 'липкой', \
				'на хрен', 'в пене', 'женской', 'жаждет'],
			['красоты.', 'мерзлоты.', 'суеты.', 'наркоты.', 'срамоты.', \
				'школоты.', 'типа ты.', 'простоты.', 'хуеты.', 'наготы.']]
	msg = '\n %s' % ' '.join([random.choice(t) for t in dict])
	msg = '\n'.join(t.strip() for t in msg.split('\n'))
	send_msg(raw_in, msg)

commands = [['poem', cmd_poem, False, 'raw', 'Just funny poem.']]

# The end is near!
