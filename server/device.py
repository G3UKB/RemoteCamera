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

# System imports
from time import sleep

# Application imports
from defs import *

# Import the Adafruit lib
import Adafruit_PCA9685

"""
Device class implements low level servo interface
"""
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
        self.__el_servo_min = 190
        self.__el_servo_max = 400
        # Home is mid span for AZ i.e. +- 90 deg
        self.__az_home = int(((self.__az_servo_max - self.__az_servo_min)/2) + self.__az_servo_min)
        # Home is 90 deg for EL i.e. horizontal
        self.__el_home = self.__el_servo_max
        
        self.__az_value_per_degree = (self.__az_servo_max - self.__az_servo_min) / AZ_RANGE
        self.__el_value_per_degree = (self.__el_servo_max - self.__el_servo_min) / EL_RANGE
        
        # Best for servos
        self.__device.set_pwm_freq(60)
        
        # Send home
        self.__device.set_pwm(AZ, 0, self.__az_home)
        self.__device.set_pwm(EL, 0, self.__el_home)
        
        # Set home values as datum
        self.__az_val = self.__az_home
        self.__el_val = self.__el_home
    
    #------------------------------------------------------------------
    # PUBLIC
    def home(self):
        """
        Move az and el to the home position.
        
        Arguments:
        
        """
        
        # Send home
        # AZ homes at 90 deg
        self.__device.move(AZ, 90)
        # EL homes at 0 deg
        self.__device.move(EL, 0)
        
    def move(self, ch, deg):
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
            pos = int((self.__az_value_per_degree * deg) + self.__az_servo_min)
            if pos >= self.__az_servo_min and pos <= self.__az_servo_max:
                self.__move(AZ, pos)
            else:
                print("Invalid AZ pos %d" % pos)
        else:
            deg = EL_RANGE - deg
            pos = int((self.__el_value_per_degree * deg) + self.__el_servo_min)
            if pos >= self.__el_servo_min and pos <= self.__el_servo_max:
                self.__move(EL, pos)
            else:
                print("Invalid EL pos %d" % pos)
                
    #------------------------------------------------------------------
    # PRIVATE
    def __move(self, ch, value):
        """
        Move implementation
        
        Arguments:
            ch  --  channel to move AZ, EL
            value   --  value to move to
        """
        
        if ch == AZ:
            # Determine move direction
            if value > self.__az_val:
                inc = 5
            else:
                inc = -5
            # Move incrementally from where we are to destination
            for n in range(self.__az_val, value, inc):
                self.__device.set_pwm(ch, 0, n)
                sleep(0.1)
            # Make sure wea arrive
            self.__device.set_pwm(ch, 0, value)
            # Save new position
            self.__az_val = value
        else:
            # Ditto for EL
            if value > self.__el_val:
                inc = 5
            else:
                inc = -5
            for n in range(self.__el_val, value, inc):
                self.__device.set_pwm(ch, 0, n)
                sleep(0.1)
            self.__device.set_pwm(ch, 0, value)
            self.__el_val = value

#------------------------------------------------------------------
# Test Entry point            
if __name__ == '__main__':
    dev = Device()
    dev.move(0,20)
    dev.move(1,20)
    sleep(3)
    dev.move(0,0)
    dev.move(1,0)
    
