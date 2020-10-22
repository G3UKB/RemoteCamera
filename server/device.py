#!/usr/bin/env python3
#
# device.py
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

"""
----------------------------------------------------------------------
 Controls the remote camera azimuth and elevation using a simple 2 servo controller.
 RobotShop:
     1. Lynxmotion Large Pan / Tilt Kit
     2. HS-645MG Servo Motor (Azimuth rotator)
     3. HS-805BB Giant Scale Servo Motor (Elevation)
 Servo Controller:     Adafruit 16-Channel 12-bit PWM/Servo Driver - I2C interface - PCA9685
 
 Note, you can't slow down a servo, they will go full pelt so the strategy is to move
 incrementally with a delay. With small increments this can appear smooth.
----------------------------------------------------------------------
"""

# Import the Adafruit lib
import Adafruit_PCA9685

AZ = 0
EL = 1
AZ_RANGE = 180
EL_RANGE = 90

class Device:
    
    def __init__(self):
        """
        Constructor
        
        Arguments:
        
        """
        
        # Initialise the library
        self.__device = Adafruit_PCA9685.PCA9685()
        
        # Tweek for the correct range
        self.__az_servo_min = 150
        self.__az_servo_max = 600
        self.__el_servo_min = 150
        self.__el_servo_max = 600
        
        self.__az_value_per_degree = (self.__az_servo_max - self.__az_servo_min) / AZ_RANGE
        self.__el_value_per_degree = (self.__el_servo_max - self.__el_servo_min) / EL_RANGE
        
        # Best for servos
        self.__device.set_pwm_freq(60)
        
    def move(self, ch, deg)
        """
        Move az or el to the given position.
        
        Arguments:
        ch  --  AZ or EL
        deg --  degrees to move to -
                    az: 0 - 180
                    el: 0 - 90
                Note that el is inverted i.e we want 0 deg
                to be camera facing forward which is servo at 90 deg.
                
        """
        
        if ch == AZ:
            self.__move(AZ, self.__az_value_per_degree * deg)
        else:
            self.__move(EL, self.__el_value_per_degree * deg)
    
    def __move(self, sc, value):
        
        for n in range(value):
            pwm.set_pwm(ch, 0, n)
            sleep(0.01)
            
# Test Entry point            
if __name__ == '__main__':
    dev = Device()
    dev.move(0,0)
    dev.move(1,0)