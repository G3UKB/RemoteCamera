#!/usr/bin/env python3
#
# camera_client.py
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

import os, sys
import threading
import socket
import pickle
import platform
import subprocess
import traceback
from time import sleep

# PyQt5 imports
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QPen, QFont
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QFrame, QGroupBox, QMessageBox, QLabel, QSlider, QLineEdit, QTextEdit, QComboBox, QPushButton, QCheckBox, QRadioButton, QSpinBox, QAction, QWidget, QGridLayout

#from defs import *

CMD_PORT = 10002
SERVER_IP = '192.168.1.107'

class CameraClient(QMainWindow):
    
    def __init__(self, qt_app):
        
        super(CameraClient, self).__init__()
        
        # Create a datagram socket
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # The application
        self.__qt_app = qt_app
        
        # Set the back colour
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background,QtGui.QColor(195,195,195,255))
        self.setPalette(palette)

        # Initialise the GUI
        self.initUI()
    
    #========================================================================================    
    # UI initialisation and window event handlers
    def initUI(self):
        """ Configure the GUI interface """
        
        self.setToolTip('Remote Camera')
        
        # Arrange window
        self.setGeometry(300,300,300,200)
                         
        self.setWindowTitle('Remote Camera')
        
        #=======================================================
        # Set main layout
        w = QWidget()
        self.setCentralWidget(w)
        self.__grid = QGridLayout()
        w.setLayout(self.__grid)
        
        # Add sliders
        self.__az = QSlider(QtCore.Qt.Horizontal)
        self.__az.setMinimum(-90)
        self.__az.setMaximum(90)
        self.__az.setValue(0)
        self.__grid.addWidget(self.__az, 0,0)
        self.__az.sliderReleased.connect(self.__az_released)
        
        self.__el = QSlider(QtCore.Qt.Vertical)
        self.__el.setMinimum(0)
        self.__el.setMaximum(90)
        self.__el.setValue(0)
        self.__grid.addWidget(self.__el, 0,1)
        self.__el.sliderReleased.connect(self.__el_released)
        
        # Add buttons
        self.__btngrid = QGridLayout()
        w1 = QWidget()
        w1.setLayout(self.__btngrid)
        self.__grid.addWidget(w1, 1,0,1,2)
        self.__home = QPushButton("Home")
        self.__btngrid.addWidget(self.__home, 0,0)
        self.__home.clicked.connect(self.__do_home)
        self.__reset = QPushButton("Reset")
        self.__btngrid.addWidget(self.__reset, 0,1)
        self.__reset.clicked.connect(self.__do_reset)
        self.__exit = QPushButton("Exit")
        self.__btngrid.addWidget(self.__exit, 0,2)
        self.__exit.clicked.connect(self.__do_exit)
        
    #========================================================================================
    # Run application
    def run(self, ):
        """ Run the application """
        
        # Start idle processing
        #QtCore.QTimer.singleShot(IDLE_TICKER, self.__idleProcessing)
        
        # Returns when application exits
        # Show the GUI
        self.show()
        self.repaint()
        
        # Start streaming
        self.__sock.sendto(pickle.dumps(['CMD_STREAM_START']), (SERVER_IP, CMD_PORT))
        sleep(2)
        
        # Start VLC
        # Run command in a new shell
        if platform.system().lower() == 'linux' or platform == 'linux2':
            self.__vlc = subprocess.Popen(["vlc", "rtsp://%s:8554/" % SERVER_IP], shell=False)
        else:
            self.__vlc = subprocess.Popen("C:/Program Files (x86)/VideoLAN/VLC/vlc.exe rtsp://%s:8554/" % SERVER_IP, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=False)
    
        # Enter event loop
        return self.__qt_app.exec_()    
    
    #=======================================================
    # Window events
    def closeEvent(self, event):

        self.__close()
    
    def __close(self):
        # Stop streaming
        self.__sock.sendto(pickle.dumps(['CMD_STREAM_STOP']), (SERVER_IP, CMD_PORT))
        sleep(2)
        # Close VNC
        if platform.system().lower() == 'linux' or platform == 'linux2':
            child = subprocess.Popen('pgrep -x vlc', stdout=subprocess.PIPE, shell=True)
            result = child.communicate()[0]
            vlc_pid = result.decode('utf-8')
            os.kill (int(vlc_pid), 9)
        else:
            self.__vlc.terminate()
        # close socket
        self.__sock.close()
    
    def __do_home(self):
        self.__sock.sendto(pickle.dumps(['CMD_HOME']), (SERVER_IP, CMD_PORT))
    
    def __do_reset(self):
        self.__sock.sendto(pickle.dumps(['CMD_RESET']), (SERVER_IP, CMD_PORT))

    def __do_exit(self):
        self.__close()
        sys.exit()
        
    #=======================================================
    # Track azimuth
    def __az_released(self):
    
        # Value ranges -90 to +90
        # Map this to 0 - 180 degrees
        val = self.__az.value()
        val= val + 90
        self.__sock.sendto(pickle.dumps(['CMD_MOVE', 0, val]), (SERVER_IP, CMD_PORT))
    
    #=======================================================
    # Track elevation
    def __el_released(self):
    
        # Value ranges 0 to +90
        val = self.__el.value()
        self.__sock.sendto(pickle.dumps(['CMD_MOVE', 1, val]), (SERVER_IP, CMD_PORT))
        
#======================================================================================================================
# Main code
def main():
    
    try:
        # The one and only QApplication 
        qt_app = QApplication(sys.argv)
        # Crete instance
        client = CameraClient(qt_app)
        # Run application loop
        sys.exit(client.run())
       
    except Exception as e:
        print ('Exception [%s][%s]' % (str(e), traceback.format_exc()))
 
# Entry point       
if __name__ == '__main__':
    main()