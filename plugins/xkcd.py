#!/usr/bin/python
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

def cmd_xkcd(raw_in):
    try:
        data = load_page('http://xkcd.ru/random/')
        ttl = re.search('<h1>(.*?)</h1>', data).group(1)
        img = re.search('http://xkcd.ru/i/.*?.png', data).group(0)
        txt = unhtml_hard(re.search('<div class="comics_text">(.*?)</div>', data).group(1))
        msg = '<a href="%s">%s</a>\n%s' % (img, ttl, txt)
    except:
        msg = 'Error!'
    send_msg(raw_in, msg)

commands = [['xkcd', cmd_xkcd, False, 'raw', 'Show random picture from xkcd.ru']]

# The end is near!
