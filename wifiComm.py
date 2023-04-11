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

class wifiArduino(QThread):
    send2Plot = pyqtSignal(list)
    send2SerialMonitor = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.host = '192.168.1.83'  # '192.168.4.2' # Use static addresses for both ESp32 and laptop/computer
        self.port = 7394        # Communication port number: Has to be same as used in ESP32/Arduino
        self.bufferSize = 255
        self.serialFileWrite = fIO.DataFileIO()

    def setupWifi(self):
        try:
            self.wifiCon = skt.socket(skt.AF_INET, skt.SOCK_DGRAM, skt.IPPROTO_UDP)
            self.wifiCon.setsockopt(skt.SOL_SOCKET, skt.SO_REUSEADDR, 1)
        except skt.error:
            print('Failed to create socket.')  # Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            return False
        try:  # Bind to IP Address and Port
            self.wifiCon.bind((self.host, self.port))
        except skt.error:
            print('Bind failed. Error: ')  # + str(msg[0]) + ': ' + msg[1])
            return False
        print('Server listening')
        return self.handshake()
        # return True

    def handshake(self):
        start_time = time.time()
        while True:
            (message, self.clientIP) = self.wifiCon.recvfrom(self.bufferSize)
            lenHand = min(9,len(message))
            lenConn = min(22,len(message))
            if message[:lenHand] == b'Handshake':
                self.wifiCon.sendto(b'Handshake Server', self.clientIP)
                print("Handshake signal obtained")
            elif message[:lenConn] == b'Connection established':
                print("Connection established")
                return True
            else:
                dataIn = message.decode('ASCII').strip()
                dataList = dataIn.split(',')
                if len(dataList) >= 10:
                    return True
            curr_time = time.time()
            if curr_time - start_time >= 2:
                return False


    def run(self):
        """This loop should run continuously"""
        currTime = time.time()
        while True:
            (message, address) = self.wifiCon.recvfrom(self.bufferSize)
            dataIn = message.decode('ASCII').strip()
            dataIn = dataIn.rstrip('\x00')
            dataList = dataIn.split(',')
            isNum, numList = self.numerize(dataList)
            if len(dataList) >= 10:  # If the data is actual data (with sensors heaters and the like)
                self.serialFileWrite.writeData(dataList)
                if isNum:
                    self.send2Plot.emit(numList)
            else:  # This part is when the data is less than 10 parts. #TODO Process the data properly
                self.send2SerialMonitor.emit(dataIn)

    def getData(self):
        pass

    def write(self, sendStr):
        bytes2Send = sendStr.encode()
        print(bytes2Send)
        self.wifiCon.sendto(bytes2Send, self.clientIP)

    def numerize(self, textList):
        numList = []
        isNum = True
        for data in textList:
            data = data.strip()
            if (not data):
                continue
            try:
                flData = float(data)
                intData = int(flData)
                if intData == flData:
                    numList = numList + [intData]
                else:
                    numList = numList + [flData]
            except:
                numList = numList + [data]
                isNum = False
        return isNum, numList