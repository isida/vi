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

def cmd_update(raw_in):
	send_msg(raw_in,'Let\'s update!')
	check_updates()
	sys.exit('update')
	
def cmd_restart(raw_in):
	send_msg(raw_in,'Let\'s restart!')
	check_updates()
	sys.exit('restart')

def cmd_quit(raw_in):
	send_msg(raw_in,'See Ya!')
	check_updates()
	sys.exit('exit')

commands = [['update', cmd_update, True, 'raw', 'Update bot from repository.'],
			['restart', cmd_restart, True, 'raw', 'Restart bot.'],
			['quit', cmd_quit, True, 'raw', 'Shutdown bot.']]

# The end is near!
