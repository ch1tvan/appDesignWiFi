
from PyQt5.QtCore import pyqtSignal, QThread
import pyqtgraph as pg
import time

class dataPlotter(QThread):

    def __init__(self, super_widget, sensorList):
        super().__init__()
        self.plotData = pg.GraphicsLayoutWidget(super_widget)
        self.plotData.setAutoFillBackground(True)
        self.plotData.setBackground('w')  # Set the background color of the layout widget
        self.initializePlotData(sensorList)

    def initializePlotData(self, sensorList):
        self.num_points = 1000
        self.window_size = 40
        self.startTime = time.time()
        self.prevTime = self.startTime
        self.currTime = self.prevTime
        self.numSensors = len(sensorList)
        # self.xT = [0.0] * num_points
        # self.ySenData = [[0] * self.num_points for i in range(self.numSensors)]
        self.xT = [0.0]
        self.ySenData = [[0] for i in range(self.numSensors)]
        self.ySenAvg = [[0] for i in range(self.numSensors)]
        self.currIND = 0
        # Setup Subplots for Sensors 1 and 2
        p1 = self.setup_plot_item()
        # Add Title
        p1.setTitle(sensorList[0] + " and " + sensorList[1], color="b", size="13pt")
        pen = [pg.mkPen(color=(200, 0, 0)), pg.mkPen(color=(0, 0, 200)), pg.mkPen(color=(0, 200, 0))]  # TODO: look into what else the pen is capable of besides line color
        penDil = [pg.mkPen(color=(200, 0, 0, 0.5)), pg.mkPen(color=(0, 0, 200, 0.5)), pg.mkPen(color=(0, 200, 0, 0.5))]
        self.data_line_S1 = []
        self.data_line_S1_avg = []
        for i in range(self.numSensors):
            # self.data_line_S1 = p1.plot(self.xT, self.ySenData[i], pen=pen)
            tempDataLine = p1.plot(self.xT, self.ySenData[i], pen=penDil[i])
            self.data_line_S1.append(tempDataLine)
            tempDataLine = p1.plot(self.xT, self.ySenAvg[i], pen=pen[i])
            self.data_line_S1_avg.append(tempDataLine)
        # pen = pg.mkPen('b')
        # self.data_line_S2 = p1.plot(self.xT, self.ySenData[1], pen=pen)
        self.plotData.addItem(p1)


    def setup_plot_item(self):
        """
        Custom function to do required settings for the plots
        it creates and returns a plot item with some settings
        Currently initialized for only digital health sensors data.
        """
        plotHandle = pg.PlotItem()
        # plotHandle.setYRange(0, 1024, padding=0)

        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "12px"}
        plotHandle.setLabel("left", "Units (U)", **styles)
        plotHandle.setLabel("bottom", "Elapsed Time (s)", **styles)
        return plotHandle

    def update_plot_data(self, dataList):
        """
        Update the plot without buffer logic
        Currently done for only Digital Health Sensors data.
        """
        # Check if max size is reached or whether it is still the start point
        delCondition = len(self.xT) >= self.num_points or self.xT[0] == 0.0
        self.currTime = time.time()
        if delCondition:
            del self.xT[0]

        self.xT.append(time.time() - self.startTime)
        for i in range(self.numSensors):
            if delCondition:
                del self.ySenData[i][0]
                del self.ySenAvg[i][0]
            self.ySenData[i].append(dataList[i])
            buffer = self.ySenData[i][-self.window_size:]
            self.ySenAvg[i].append(sum(buffer)/len(buffer))
            self.data_line_S1[i].setData(self.xT, self.ySenData[i])
            print( self.currTime - self.prevTime )
            self.data_line_S1_avg[i].setData(self.xT, self.ySenAvg[i])
        self.currIND = self.currIND + 1


        # self.data_line_S1.setData(self.xT, self.ySenData[0])
        # self.data_line_S1.setData(self.xT, self.ySenData[1])
        # self.data_line_S3.setData(self.xT, self.ySenData[1])