# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designImage.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1188, 845)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Image6 = PlotWidget(self.tab)
        self.Image6.setBaseSize(QtCore.QSize(0, 600))
        self.Image6.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Image6.setObjectName("Image6")
        self.gridLayout_2.addWidget(self.Image6, 3, 1, 1, 1)
        self.Image7 = PlotWidget(self.tab)
        self.Image7.setBaseSize(QtCore.QSize(0, 600))
        self.Image7.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Image7.setObjectName("Image7")
        self.gridLayout_2.addWidget(self.Image7, 3, 2, 1, 1)
        self.Image8 = PlotWidget(self.tab)
        self.Image8.setBaseSize(QtCore.QSize(0, 600))
        self.Image8.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Image8.setObjectName("Image8")
        self.gridLayout_2.addWidget(self.Image8, 3, 3, 1, 1)
        self.Image1 = PlotWidget(self.tab)
        self.Image1.setBaseSize(QtCore.QSize(0, 600))
        self.Image1.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Image1.setObjectName("Image1")
        self.gridLayout_2.addWidget(self.Image1, 2, 0, 1, 1)
        self.Image2 = PlotWidget(self.tab)
        self.Image2.setBaseSize(QtCore.QSize(0, 600))
        self.Image2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Image2.setObjectName("Image2")
        self.gridLayout_2.addWidget(self.Image2, 2, 1, 1, 1)
        self.Image3 = PlotWidget(self.tab)
        self.Image3.setBaseSize(QtCore.QSize(0, 600))
        self.Image3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Image3.setObjectName("Image3")
        self.gridLayout_2.addWidget(self.Image3, 2, 2, 1, 1)
        self.Image5 = PlotWidget(self.tab)
        self.Image5.setBaseSize(QtCore.QSize(0, 600))
        self.Image5.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Image5.setObjectName("Image5")
        self.gridLayout_2.addWidget(self.Image5, 3, 0, 1, 1)
        self.Image4 = PlotWidget(self.tab)
        self.Image4.setBaseSize(QtCore.QSize(0, 600))
        self.Image4.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Image4.setObjectName("Image4")
        self.gridLayout_2.addWidget(self.Image4, 2, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.browseImage = QtWidgets.QPushButton(self.tab)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.browseImage.setFont(font)
        self.browseImage.setObjectName("browseImage")
        self.gridLayout_2.addWidget(self.browseImage, 1, 3, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1188, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "JPEG decompression"))
        self.browseImage.setText(_translate("MainWindow", "Browse Image"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "JPEG"))

from pyqtgraph import PlotWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

