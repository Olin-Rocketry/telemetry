from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5 import QtCore
import numpy as np
import pyqtgraph as pg
import numpy as np
from random import randint





class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True



    def run(self):
        # set up video capture, use 0 for webcam and 1 for FPV feed
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()

            if ret:
                self.change_pixmap_signal.emit(cv_img)

        # shut down capture system
        cap.release()



    def stop(self):
        # Sets run flag to False and waits for thread to finish
        self._run_flag = False
        self.wait()





class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")

        # add video
        self.disply_width = 450
        self.display_height = 450

        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)

        # create a text label
        self.textLabel = QLabel('Webcam')

        # add live plot
        self.graphWidget = pg.PlotWidget()
        self.graphWidget2 = pg.PlotWidget()
        self.graphWidget3 = pg.PlotWidget()

        # start w/bogus data b/c making a buffer is too hard
        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points

        self.x2 = list(range(100))  # 100 time points
        self.y2 = [randint(0,100) for _ in range(100)]  # 100 data points

        self.x3 = list(range(100))  # 100 time points
        self.y3 = [randint(0,100) for _ in range(100)]  # 100 data points

        # setting background of live plotters
        self.graphWidget.setBackground('w')
        self.graphWidget2.setBackground('w')
        self.graphWidget3.setBackground('w')

        # changing line color to red
        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        self.data_line2 =  self.graphWidget2.plot(self.x2, self.y2, pen=pen)
        self.data_line3 =  self.graphWidget3.plot(self.x3, self.y3, pen=pen)

        # some QT stuff
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()


        # create a vertical box layout and add the two labels
        vbox = QGridLayout()
        self.setLayout(vbox)
        vbox.addWidget(self.image_label, 0,0)

        # vbox.addWidget(self.textLabel)
        self.graphWidget.setFixedWidth(400)

        self.graphWidget.setFixedHeight(400)

        self.graphWidget.setTitle("Title 1", color="b", size="12pt")

        self.graphWidget2.setFixedWidth(400)

        self.graphWidget2.setFixedHeight(400)

        self.graphWidget2.setTitle("Title 2", color="b", size="12pt")

        self.graphWidget3.setFixedWidth(400)

        self.graphWidget3.setFixedHeight(400)

        self.graphWidget3.setTitle("Title 3", color="b", size="12pt")

        # self.label = QLabel('Zzzzz')



        vbox.addWidget(self.graphWidget,0,1,1,1)

        vbox.addWidget(self.graphWidget2,0,2,1,1)

        vbox.addWidget(self.graphWidget3,1,0,1,1)

        vbox.setColumnMinimumWidth(0,400)

        vbox.setColumnMinimumWidth(1,400)

        vbox.setColumnMinimumWidth(2,400)

        vbox.setRowMinimumHeight(0,400)

        # vbox.addWidget(self.label, 0,3)

        # set the vbox layout as the widgets layout

        # self.setLayout(vbox)



        # create the video capture thread
        self.thread = VideoThread()

        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)

        # start the thread
        self.thread.start()



    def closeEvent(self, event):

        self.thread.stop()

        event.accept()



    def update_plot_data(self):



        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.
        self.y = self.y[1:]  # Remove the first 
        self.y.append( randint(0,100))  # Add a new random value.
        self.data_line.setData(self.x, self.y)  # Update the data.



        self.x2 = self.x2[1:]  # Remove the first y element.
        self.x2.append(self.x2[-1] + 1)  # Add a new value 1 higher than the last.
        self.y2 = self.y2[1:]  # Remove the first 
        self.y2.append( randint(0,100))  # Add a new random value.
        self.data_line2.setData(self.x2, self.y2)  # Update the data.


        self.x3 = self.x3[1:]  # Remove the first y element.
        self.x3.append(self.x3[-1] + 1)  # Add a new value 1 higher than the last.
        self.y3 = self.y3[1:]  # Remove the first 
        self.y3.append( randint(0,100))  # Add a new random value.
        self.data_line3.setData(self.x3, self.y3)  # Update the data.



    @pyqtSlot(np.ndarray)

    def update_image(self, cv_img):

        """Updates the image_label with a new opencv image"""

        qt_img = self.convert_cv_qt(cv_img)

        self.image_label.setPixmap(qt_img)

    

    def convert_cv_qt(self, cv_img):

        """Convert from an opencv image to QPixmap"""

        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

        h, w, ch = rgb_image.shape

        bytes_per_line = ch * w

        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)

        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)

        return QPixmap.fromImage(p)

    

if __name__=="__main__":

    app = QApplication(sys.argv)

    a = App()

    a.show()

    sys.exit(app.exec_())