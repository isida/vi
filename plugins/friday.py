#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    iSida bot VI plugin                                                      #
#    Copyright (C) VitaliyS <hetleven@yandex.ua>                                    #
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

def cmd_friday(raw_in):
    day = datetime.datetime.isoweekday(datetime.datetime.now())
    date_file = DATA_FOLDER % 'friday.txt'
    if os.path.isfile(date_file):
        frases = readfile(date_file).decode('UTF')
        frases = map(lambda x: x.split(' || '), frases.split('\n'))
        week = [u'понедельник', u'вторник', u'среда', u'четверг', u'пятница', u'суббота', u'воскресенье']
        if not frases:
            msg = 'Read file error.'
        else:
            frs = [i[0] for i in frases if str(day) in i[1]]
            msg = random.choice(frs)
            if 'user' in msg:
                msg = msg.replace('user', raw_in['message']['from'].get('username',''))
            if 'yesterday' in msg:
                msg = msg.replace('yesterday', week[(day + 5) % 7])
            if 'tomorrow' in msg:
                msg = msg.replace('tomorrow', week[day % 7])
    else:
        msg = 'Database doesn\'t exist.'
    send_msg(raw_in, msg)


commands = [['friday', cmd_friday, False, 'raw', 'Today is Friday']]

# The end is near!
