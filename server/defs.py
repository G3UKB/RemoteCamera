#!/usr/bin/env python3
#
# defa.py
# 
# Copyright (C) 2017 by G3UKB Bob Cowdery
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#    
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#    
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#    
#  The author can be reached by email at:   
#     bob@bobcowdery.plus.com
#

# Constants
AZ = 0
EL = 1
AZ_RANGE = 180
EL_RANGE = 90

# Net interface
RQST_IP = ''
RQST_PORT = 10002

# Command types
CMD_HOME = 'CMD_HOME'
CMD_MOVE = 'CMD_MOVE'
CMD_RESET = 'CMD_RESET'
CMD_STREAM_START = 'CMD_STREAM_START'
CMD_STREAM_STOP = 'CMD_STREAM_STOP'
