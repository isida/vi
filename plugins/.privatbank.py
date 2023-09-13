#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    iSida bot VI plugin                                                      #
#    Copyright (C) VitaliyS <hetleven@yandex.ua>                              #
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

def cmd_pbrate(raw_in):
    try:
        data = load_page('https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5')
        res = re.findall('<exchangerate ccy="(.*?)" base_ccy=".*?" buy="(\d*\.\d*)0*" sale="(\d*\.\d*)0*"/>', data)
        msg = '<b>Privatbank exchange rates</b>\n<pre>Сurrency    Buy      Sale'
        cico = {'RUR': '🇷🇺', 'USD': '🇺🇸', 'EUR': '🇫🇲', 'BTC': '💰'}
        for i in res:
            base_ccy = cico.get(i[0], '🔵') + i[0]
            buy = round(float(i[1]), 2)
            sale = round(float(i[2]), 2)
            msg += '\n%s      %-7s  %-7s' % (base_ccy, buy, sale)
        msg += '</pre>'
    except:
        msg = 'Ooops! The market collapsed, the salary will not be!'
    send_msg(raw_in, msg)

commands = [['pbrate', cmd_pbrate, False, 'raw', 'Privatbank exchange rate']]

# The end is near!
