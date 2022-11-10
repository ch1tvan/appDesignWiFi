# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'appDesignWithPlots.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from serialArduino_v2 import *
from fileIO_v1 import *
from dataPlotter import *

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 660)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Setup File IO
        self.dataCommentWriter = DataFileIO()
        self.commandComment = listFileIO()
        commandDict = self.commandComment.readCommandDict()
        commentDict = self.commandComment.readCommentDict()

        # Horizontal Layout for Selecting Command and Comment
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 30, 600, 210))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.selectionLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.selectionLayout.setContentsMargins(0, 0, 0, 0)
        self.selectionLayout.setSpacing(30)
        self.selectionLayout.setObjectName("selectionLayout")

        # Command List
        self.commandList = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.commandList.setFont(font)
        self.commandList.setObjectName("commandList")
        self.selectionLayout.addWidget(self.commandList)
        self.commandList.doubleClicked.connect(lambda: self.commandSelected())
        self.commandLine = commandDict.get(0)
        self.commandLine = [data.strip() for data in self.commandLine]
        self.commandArd = commandDict.get(1)
        self.commandArd = [data.strip() for data in self.commandArd]
        self.commandList.addItems(self.commandLine)

        # Comment List
        self.commentList = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.commentList.setFont(font)
        self.commentList.setObjectName("commentList")
        self.selectionLayout.addWidget(self.commentList)
        self.commentList.doubleClicked.connect(lambda: self.commentSelected())
        self.commentLine = commentDict.get(0)
        self.commentLine = [data.strip() for data in self.commentLine]
        self.commentFile = commentDict.get(1)
        self.commentFile = [data.strip() for data in self.commentFile]
        self.commentList.addItems(self.commentLine)

        # Horizontal Layout for Text inputs for command and comments
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(30, 250, 600, 30))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.inputLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.inputLayout.setContentsMargins(0, 0, 0, 0)
        self.inputLayout.setSpacing(30)
        self.inputLayout.setObjectName("inputLayout")

        # Input for the command
        self.inputCommand = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.inputCommand.setFont(font)
        self.inputCommand.setObjectName("inputCommand")
        self.inputLayout.addWidget(self.inputCommand)
        self.inputCommand.setPlaceholderText("Enter Command in form of ID;Com")
        self.inputCommand.returnPressed.connect(lambda: self.manualCommandIn())

        # Input for comment
        self.inputComment = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.inputComment.setFont(font)
        self.inputComment.setObjectName("inputComment")
        self.inputLayout.addWidget(self.inputComment)
        self.inputComment.setPlaceholderText("Enter Comment in form of Com;ID")
        self.inputComment.returnPressed.connect(lambda: self.manualCommentIn())

        # Horizontal Layout for Buttons
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(80, 290, 500, 40))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.buttonLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setSpacing(130)
        self.buttonLayout.setObjectName("buttonLayout")

        # Read Button
        self.readButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.readButton.setFont(font)
        self.readButton.setStyleSheet("background-color: rgb(20, 80, 20);")
        self.readButton.setObjectName("readButton")
        self.buttonLayout.addWidget(self.readButton)
        self.readButton.clicked.connect(lambda: self.readButtonPressed())

        # Stop Read Button
        self.stopButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.stopButton.setFont(font)
        self.stopButton.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.stopButton.setObjectName("stopButton")
        self.buttonLayout.addWidget(self.stopButton)
        self.stopButton.clicked.connect(lambda: self.stopButtonPressed())

        # Serial Monitor for the time being
        self.serialMonitor = QtWidgets.QTextEdit(self.centralwidget)
        self.serialMonitor.setGeometry(QtCore.QRect(670, 30, 300, 298))
        self.serialMonitor.setObjectName("serialMonitor")
        self.serialMonitor.setReadOnly(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.serialMonitor.setFont(font)
        self.serialMonitor.document().setMaximumBlockCount(10)

        # Plot Data
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(30, 345, 940, 280))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(100)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Plot 1
        self.plotData_1 = dataPlotter(self.horizontalLayoutWidget_4, ["Sensor 1", "Sensor 2"])
        self.plotData_1.setObjectName("plotData_1")
        self.horizontalLayout.addWidget(self.plotData_1.plotData)

        # Plot 2
        # self.plotData_2 = QtWidgets.QOpenGLWidget(self.horizontalLayoutWidget_4)
        # self.plotData_2.setAutoFillBackground(True)
        self.plotData_2 = dataPlotter(self.horizontalLayoutWidget_4, ["Sensor 3", "Sensor 4"])
        self.plotData_2.setObjectName("plotData_2")
        self.horizontalLayout.addWidget(self.plotData_2.plotData)
        # self.horizontalLayout.addWidget(self.plotData_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.setupSerial()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.readButton.setText(_translate("MainWindow", "Read"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))

    def commandSelected(self):
        currIND = self.commandList.selectedIndexes()[0].row()
        commandLine = self.commandLine[currIND]
        commandArd = self.commandArd[currIND]
        self.serialMonitor.append(datetime.now().strftime("%H:%M:%S, ") + commandLine)
        # print(commandArd)
        # print(commandLine)
        if self.isArdConnected:
            self.arduinoSer.write(commandArd)
        self.dataCommentWriter.writeComment(commandLine)

    def commentSelected(self):
        currIND = self.commentList.selectedIndexes()[0].row()
        commentLine = self.commentLine[currIND]
        commentFile = self.commentFile[currIND]
        self.serialMonitor.append(datetime.now().strftime("%H:%M:%S, ") + commentLine)
        # print(commentFile)
        # print(commentLine)
        self.dataCommentWriter.writeComment(commentFile)

    def readButtonPressed(self):
        self.readButton.setStyleSheet("background-color: rgb(0, 200, 0); color: rgb(255, 255, 255);")
        self.stopButton.setStyleSheet("background-color: rgb(80, 20, 20);")
        if self.isArdConnected:
            self.arduinoSer.write('r')
        self.serialMonitor.append(datetime.now().strftime("%H:%M:%S, ") + "Started Reading")
        self.dataCommentWriter.writeComment("Reading_Started")

    def stopButtonPressed(self):
        self.stopButton.setStyleSheet("background-color: rgb(200, 0, 0); color: rgb(255, 255, 255);")
        self.readButton.setStyleSheet("background-color: rgb(20, 80, 20); color: rgb(0, 0, 0);")
        if self.isArdConnected:
            self.arduinoSer.write('s')
        self.serialMonitor.append(datetime.now().strftime("%H:%M:%S, ") + "Stopped Reading")
        self.dataCommentWriter.writeComment("Reading_Stopped")

    def manualCommandIn(self):
        # print(self.inputCommand.text())
        tempStr = self.inputCommand.text().split(';')
        command2Arduino = tempStr[-1].strip()
        commandLine = tempStr[0].strip()
        if( len(tempStr) > 1 ):
            self.commandList.addItem(commandLine)
            self.commandComment.writeCommand2File([commandLine, command2Arduino])
            self.commandLine.append(commandLine)
            self.commandArd.append(command2Arduino)
        if self.isArdConnected:
            self.arduinoSer.write(command2Arduino)
        self.serialMonitor.append(datetime.now().strftime("%H:%M:%S, ") + commandLine)
        self.dataCommentWriter.writeComment(commandLine)
        self.inputCommand.clear()

    def manualCommentIn(self):
        # print(self.inputComment.text())
        tempStr = self.inputComment.text().split(';')
        commentLine = tempStr[0].strip()
        commentFile = tempStr[-1].strip()
        if (len(tempStr) > 1):
            self.commentList.addItem(commentLine)
            self.commandComment.writeComment2File([commentLine, commentFile])
            self.commentLine.append(commentLine)
            self.commentFile.append(commentFile)
        self.serialMonitor.append(datetime.now().strftime("%H:%M:%S, ") + commentLine)
        self.dataCommentWriter.writeComment(commentFile)
        self.inputComment.clear()

    def setupSerial(self):
        # Serial Connection Establishing
        self.arduinoSer = serialArduino()
        self.isArdConnected = self.arduinoSer.setupSerial()
        self.arduinoSer.send2Plot.connect(self.plotReceivedData)
        self.arduinoSer.send2SerialMonitor.connect(self.arduino2serData)
        if self.isArdConnected:
            self.serialMonitor.insertPlainText("Serial Connection to Arduino Established")
            self.arduinoSer.start()
        else:
            self.serialMonitor.insertPlainText("Problem with Serial Communication")

    def plotReceivedData(self, sen_data):
        self.plotData_1.update_plot_data(sen_data[5:7])
        self.plotData_2.update_plot_data(sen_data[7:9])
        # pass

    def arduino2serData(self, printData):
        self.serialMonitor.append(datetime.now().strftime("%H:%M:%S, ") + printData)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.stopButtonPressed()
    sys.exit(app.exec_())