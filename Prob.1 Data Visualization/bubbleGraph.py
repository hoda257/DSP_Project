from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox , QSlider , QLabel
import pyqtgraph as pg
import pyqtgraph.exporters
from design import Ui_Covid19
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy as np
import time
import sys
import cv2
import numpy as np
import glob


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_Covid19()
        self.ui.setupUi(self)

        self.images_path = 'Exported Video'
        self.dataset_path = 'covid_19_data.csv'
        self.corona_data = []
        self.deaths = []
        self.recovered = []
        self.confirmed_cases = []
        self.countries = []
        self.days = []
        self.i = 0
        self.j = 0
        self.shouldPlay = -1

        self.ui.BG_resume_button.clicked.connect(self.timer_function)
        self.ui.BG_slider.valueChanged.connect(self.slider_function)
        self.ui.BG_export_button.clicked.connect(self.export)


    def read_data(self):
        self.corona_data = pd.read_csv(self.dataset_path)
        self.deaths = self.corona_data['Deaths'] 
        self.recovered = self.corona_data['Recovered']
        self.confirmed_cases = self.corona_data['Confirmed']

        for day in self.corona_data['ObservationDate']:
            if day not in self.days:
                self.days.append(day)

        for country in self.corona_data['Country/Region']:
            if country not in self.countries:
                self.countries.append(country)

    def plot(self):
        if self.i != len(self.days)+1:
            self.ui.BG_plotWidget.clear()
            self.read_data()
            x = self.deaths[self.corona_data['ObservationDate'] == self.days[self.i]]
            y = self.recovered[self.corona_data['ObservationDate'] == self.days[self.i]]
            z = self.confirmed_cases[self.corona_data['ObservationDate'] == self.days[self.i]]
            self.ui.BG_plotWidget.setBackground('w')
            self.ui.BG_plotWidget.plotItem.getViewBox().setRange(xRange= (0, 40000), yRange= (0, 200000))
            self.ui.BG_plotWidget.plot(np.array(x), np.array(y), pen= None, symbol= 'o', symbolSize= np.array(z)/1000)
            self.ui.BG_plotWidget.setLabel('left', 'Recovered', color='green', size=30)
            self.ui.BG_plotWidget.setLabel('bottom', 'Deaths', color='red', size=30)
            self.ui.BG_slider.setRange(0, len(self.days)-1)
            self.ui.BG_slider_label.setText(str(self.days[self.i]))
            self.ui.BG_slider.setValue(self.i)

            exporter = pg.exporters.ImageExporter(self.ui.BG_plotWidget.plotItem)
            exporter.params.param('width').setValue(940, blockSignal=exporter.widthChanged)
            exporter.params.param('height').setValue(520, blockSignal=exporter.heightChanged)
            exporter.export(self.images_path +'/' + 'image' + str(self.i) + 'bg.png')

            self.i += 1

    def export(self):
        img_array = []
        for filename in glob.glob(self.images_path + '/' +'*bg.png'):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)

        if len(img_array) != 0:
            vidName = QtWidgets.QFileDialog.getSaveFileName(self,'savefile')
            out = cv2.VideoWriter(str(vidName[0]) + '.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
        
            for i in range(len(img_array)):
                out.write(img_array[i])
            out.release()

    def slider_function(self, value):
        self.i = value
        self.plot()
       
    def timer_function(self):
        self.shouldPlay*= -1
        if(self.shouldPlay==1): 
            self.timer = QtCore.QTimer()
            self.timer.setInterval(20)
            self.timer.timeout.connect(self.plot)
            self.timer.start(500)
        else:
            self.timer.timeout.connect(self.plot)
            self.timer.stop()
    


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()


# dataset_path = 'C:/Users/WIN 10/Downloads/Digital Signal Processing/Final Project/Data Visualization/novel-corona-virus-2019-dataset/covid_19_data.csv'
# corona_data = pd.read_csv(dataset_path)

# i =99




# data_frame = pd.DataFrame({'X': deaths[corona_data['ObservationDate'] == days[i]], 'Y': recovered[corona_data['ObservationDate'] == days[i]], 'Colors': colors, 'bubble_size': confirmed_cases[corona_data['ObservationDate'] == days[i]]})
# plt.scatter('X', 'Y', s= 'bubble_size', c= 'Colors', alpha= 0.5, data= data_frame)
# plt.show()


