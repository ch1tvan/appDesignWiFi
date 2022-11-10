import pandas as pd # for csv files
from datetime import datetime # for getting teh date and time for file names
import os
from timerInterr_v0 import *

class fileInOut():
    def __init__(self, directory, file_name):
        self.directory = directory
        self.fileName = file_name
        if not self.directory[-1] == '/':
            self.directory = self.directory + '/'
        self.fullFilename = self.directory + file_name
        self.header = None
        self.fileSetup()


    def setHeader(self, headerFlag):
        self.header = headerFlag

    def fileSetup(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        if not os.path.isfile(self.fullFilename):   # Is the first line to be written
            self.header = True

    # def getDataFrame(self, write_data):
    #     if isinstance(write_data, str):
    #         write_data = write_data.split()
    #         write_data = [i.strip() for i in write_data]
    #     tempDataFrame = pd.DataFrame([write_data])   # Convert string into dataFrame
    #     return tempDataFrame

    def write2File(self, tempDataFrame):
        # Append to the file (depending on the format
        tempDataFrame.to_csv(self.fullFilename, mode='a', index=False, header=self.header)
        if(self.header):    # First line written
            self.header = False

    def write2Params(self, tempDataFrame):
        # Append to the file (depending on the format
        tempDataFrame.to_csv(self.fullFilename, mode='a', sep=';', index=False, header=self.header)
        if(self.header):    # First line written
            self.header = False

    def readFile(self): # TODO: Check if this function is needed and change based on the requirement.
        currDataFrame = pd.read_csv(self.fullFilename, dtype=str, header=self.header)
        return currDataFrame

    def readParams(self):
        currDataFrame = pd.read_csv(self.fullFilename, dtype=str, sep=';', header=self.header)
        return currDataFrame

    # Send data in list
    def readFile2List(self):
        currDataFrame = self.readFile()
        name_list = [i[0] for i in currDataFrame]
        return name_list

# class GUIFileIO():

class DataFileIO():
    def __init__(self):
        super().__init__()
        self.createNewFiles()
        self.setupTimerInt()


    def createNewFiles(self):
        now = datetime.now()
        self.prevTime = now
        self.results_dir = '../results/AppDesignSerial/' + now.strftime("%Y-%m-%d")

        # Data from Arduino
        self.dataSaveFilename = now.strftime("%Y-%m-%d_%H-%M-%S") + '_Experiment.csv'
        self.dataWriter = fileInOut(self.results_dir, self.dataSaveFilename)
        self.dataColumns = ['DateAndTime', 'ProgramRunTime', 'Heater1', 'Heater2', 'Heater3', 'Heater4',
                            'Sensor1', 'Sensor2', 'Sensor3', 'Sensor4', 'Sensor5', 'Input', 'Time2stop']
        self.saveDataFrame = pd.DataFrame(data=None, columns=self.dataColumns)
        self.dataWriter.write2File(self.saveDataFrame)

        # Comments to write
        self.commentFilename = now.strftime("%Y-%m-%d_%H-%M-%S") + '_Comment.csv'
        self.commentWriter = fileInOut(self.results_dir, self.commentFilename)
        self.commentColumns = ['DateAndTime', 'Comment']
        self.commentDataFrame = pd.DataFrame(data=None, columns=self.commentColumns)
        self.commentWriter.write2File(self.commentDataFrame)

    def writeData(self, currList):
        if self.timerInterrupt.change_hour():
            self.createNewFiles()
        if (len(currList) > 8):
            tNow = datetime.now()
            currList.insert(0, str(tNow)[0:-5])
            self.saveDataFrame.loc[len(self.saveDataFrame)] = currList
            if (tNow-self.prevTime).seconds>0:
                self.dataWriter.write2File(self.saveDataFrame)
                self.saveDataFrame = self.saveDataFrame[0:0]

    def writeComment(self, str2Send):
        if self.timerInterrupt.change_hour():
            self.createNewFiles()
        tNow = datetime.now()
        currList = [str(tNow)[0:-5], str2Send]
        self.commentDataFrame.loc[len(self.commentDataFrame)] = currList
        self.commentWriter.write2File(self.commentDataFrame)
        self.commentDataFrame = self.commentDataFrame[0:0]

    def setupTimerInt(self):
        # Starting the timer interrupt
        self.timerInterrupt = timerInterrupt()



class listFileIO():
    def __init__(self):
        self.file_dir = './'
        # Command File that already exists
        self.commandListFilename = 'HeaterVCommand.csv'
        self.commandWriter = fileInOut(self.file_dir, self.commandListFilename)
        self.commandFrame = self.commandWriter.readParams()
        # Comment File that already exists
        self.commentListFilename = 'ExperimentDetails.csv'
        self.commentWriter = fileInOut(self.file_dir, self.commentListFilename)
        self.commentFrame = self.commentWriter.readParams()

    def readCommentDict(self):
        return self.commentFrame.to_dict('list')

    def readCommandDict(self):
        return self.commandFrame.to_dict('list')

    def writeComment2File(self, commentList):
        tempFrame = pd.DataFrame(columns=['Comment', 'ID'])
        tempFrame.loc[0] = commentList
        tempWriter = self.commentWriter.write2Params(tempFrame)

    def writeCommand2File(self, commandList):
        tempFrame = pd.DataFrame(columns=['ID', 'Command'])
        tempFrame.loc[0] = commandList
        tempWriter = self.commandWriter.write2Params(tempFrame)

# if __name__ == "__main__":
#     # Checking the serialWrite from Arduino
#
#     # Initializing part
#     now = datetime.now()
#     results_dir = './results/' + now.strftime("%Y-%m-%d")
#     dataSaveFilename = now.strftime("%Y-%m-%d_%H-%M-%S") + ' Experiment.csv'
#     dataWriter = fileInOut(results_dir, dataSaveFilename)
#
#     # Input from Arduino
#     inputFromArduino = '28, 1.10, 1.10, 1.20, 1.20, 680, 366, 844, 346, 431, 1017, -10'
#     dataColumns = ['Date and Time', 'Program Run Time', 'Heater 1', 'Heater 2', 'Heater 3', 'Heater 4',
#                    'Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5', 'Input', 'Time to stop']
#     now = datetime.now()
#     arduinoDataList = inputFromArduino.split(', ')
#     arduinoDataList = [float(x) for x in arduinoDataList]
#     arduinoDataDict = dict(zip(dataColumns[1:],arduinoDataList))
#     arduinoDataFrame = dataWriter.getDataFrame(arduinoDataDict)
#     arduinoDataFrame.insert(0, dataColumns[0], now)
#     dataWriter.write2File(arduinoDataFrame)

