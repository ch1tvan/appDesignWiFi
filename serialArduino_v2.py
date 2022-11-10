import sys
import serial
from serial.tools import list_ports
import time
from PyQt5.QtCore import pyqtSignal, QThread
import fileIO_v1 as fIO


class serialArduino(QThread):
    send2Plot = pyqtSignal(list)
    send2SerialMonitor = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # self.BAUD = [9600, 57600, 115200]
        self.BAUD = [57600, 115200]
        # self.BAUD = [115200]
        self.ser = None
        self.dataIn = list()
        self.dataIsReady = False
        self.serialFileWrite = fIO.DataFileIO()

    # Setting the serial port by going through all potential ports from 0 to 256
    def setupSerial(self):
        portList = list_ports.comports()
        for port in portList:
            portName = port.name
            if portName.startswith('COM'):
                for baudRate in self.BAUD:
                    self.ser = serial.Serial(portName, baudrate=baudRate, timeout=1)
                    if self.handshake():
                        # self.send2SerialMonitor.emit("Connection Established")
                        return True
                    self.ser.close()
                    time.sleep(0.1)
        # self.send2SerialMonitor.emit("No Connection Found!")
        return False

    # Checking for presence of Arduino and tries to establish connection
    def handshake(self):
        start_time = time.time()
        # try:
        self.ser.flush()
        data_str = ""
        while 1:
            if self.ser.in_waiting > 0:
                # data_str = self.ser.readline()
                currRead = self.ser.read()
                # print(currRead)
                try:
                    currRead = currRead.decode('ascii')
                    data_str = data_str + currRead
                    if(data_str[-1]!='\n'):
                        continue
                except Exception as e:
                    # Print the exception
                    # print(e)
                    return False
                data_str = data_str.rstrip()
                if data_str == 'Handshake A':
                # if data_str.len > 12:
                    self.ser.write(b'Handshake B\n')
                    data_str = ""
                elif data_str == 'Connection established':
                    # print(data_str)
                    return True
            curr_time = time.time()
            # print(curr_time-start_time)
            if curr_time - start_time >= 0.7:
                return False
        # except:
        #     return False

    def run(self):
        """ Method to call data from the serial """
        currTime = time.time()
        # self.send2SerialMonitor.emit("Thread Run")
        while True:
            if self.ser.in_waiting:
                self.dataIn = self.ser.readline().decode('ascii').strip()
                self.dataIsReady = True
            if (self.dataIsReady):
                dataList = self.dataIn.split(',')
                isNum, numList = self.numerize(dataList)
                if len(dataList) >= 10:  # If the data is actual data (with sensors heaters and the like)
                    self.serialFileWrite.writeData(dataList)
                    if isNum:
                        self.send2Plot.emit(numList)
                else:  # This part is when the data is less than 10 parts. #TODO Process the data properly
                    self.send2SerialMonitor.emit(self.dataIn)
                self.dataIn = ""
                self.dataIsReady = False

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

    # def stop(self):
    #     print("Thread Stopping")
    #     self._stop_event.set()
    #
    # def stopped(self):
    #     return self._stop_event.is_set()

    def getData(self):
        self.dataIsReady = False
        return (self.dataIn)

    def write(self, sendStr):
        sendStr = (sendStr + "\n").encode()
        self.ser.write(sendStr)


if __name__ == "__main__":
    arduinoSer = serialArduino()
    isSerConnected = arduinoSer.setupSerial()
    print(isSerConnected)
    arduinoSer.start()
