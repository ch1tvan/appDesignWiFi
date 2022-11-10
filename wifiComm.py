'''
# Python UDP Server to listen to incoming connections from MAX's Toys

# This python script listens on UDP port 7394
# for messages from the ESP32 board and prints them

# References
https://docs.python.org/2/howto/sockets.html
esp32 examples

'''

import socket as skt
import sys
import time
from PyQt5.QtCore import pyqtSignal, QThread
import fileIO_v1 as fIO

class serialArduino(QThread):
    send2Plot = pyqtSignal(list)
    send2SerialMonitor = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.host = '192.168.1.80'  # '192.168.4.2' # Use static addresses for both ESp32 and laptop/computer
        self.port = 7394        # Communication port number: Has to be same as used in ESP32/Arduino

    def setupWifi(self):
        try:
            self.wifiCon = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
            self.wifiCon.setsockopt(skt.SOL_SOCKET, skt.SO_REUSEADDR, 1)
        except skt.error:
            print('Failed to create socket.')  # Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            return False
        try:
            self.wifiCon.bind(self.host, self.port)
        except skt.error:
            print('Bind failed. Error: ')  # + str(msg[0]) + ': ' + msg[1])
            return False
        print('Server listening')
        return True

    def handshake(self):
        pass

    def run(self):
        pass

    def getData(self):
        pass

    def write(self, sendStr):
        pass


while 1:
    d, a = s.recvfrom(1024)
    data = d[0]

    # s.sendto("send stuff", a)
    if not data:
        break

    print(d)

s.close()
