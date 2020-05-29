from PyQt5 import QtWidgets , QtCore
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QUrl, QDirIterator, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QFileDialog, QAction, QHBoxLayout, QVBoxLayout, QSlider,QMessageBox
from pyqtgraph import PlotWidget, plot, PlotItem
from piano import Ui_MainWindow
import numpy as np
import pyqtgraph as pg
import sys,os
import music21
from music21 import note, stream, pitch, duration, instrument, tempo, chord
from music21.note import Note, Rest
from music21.chord import Chord
from music21 import midi
import simpleaudio as sa


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        pg.setConfigOption('background', 'k')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #//////////////////// Piano Buttons //////////////////////
        self.ui.Piano1.clicked.connect(lambda : self.playNote('C4'))
        self.ui.Piano2.clicked.connect(lambda : self.playNote('C#4'))
        self.ui.Piano3.clicked.connect(lambda : self.playNote('D4'))
        self.ui.Piano4.clicked.connect(lambda : self.playNote('D#4'))
        self.ui.Piano5.clicked.connect(lambda : self.playNote('E4'))
        self.ui.Piano6.clicked.connect(lambda : self.playNote('F4'))
        self.ui.Piano7.clicked.connect(lambda : self.playNote('F#4'))
        self.ui.Piano8.clicked.connect(lambda : self.playNote('G4'))
        self.ui.Piano9.clicked.connect(lambda : self.playNote('G#4'))

        #//////////////////// Xylophone Buttons //////////////////////
        self.ui.Xylophone1.clicked.connect(lambda : self.playNote('C7'))
        self.ui.Xylophone2.clicked.connect(lambda : self.playNote('C#7'))
        self.ui.Xylophone3.clicked.connect(lambda : self.playNote('D7'))
        self.ui.Xylophone4.clicked.connect(lambda : self.playNote('D#7'))
        self.ui.Xylophone5.clicked.connect(lambda : self.playNote('E7'))
        self.ui.Xylophone6.clicked.connect(lambda : self.playNote('E#7'))
        self.ui.Xylophone7.clicked.connect(lambda : self.playNote('F#7'))
#------------------------------------------------------------------------------------------------------------------------
   
    #////////////////////////////// Play Note /////////////////////////////////////
    def playNote(self,note):
        p= Note(note)
        p.quarterLength = 1.5
        stream_obj = stream.Stream()
        stream_obj.append(p)
        sp = midi.realtime.StreamPlayer(stream_obj)
        sp.play()
#------------------------------------------------------------------------------------------------------------------------

#////////////////////////////// Main /////////////////////////////////////

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()

if __name__ == "__main__":
    main()
#------------------------------------------------------------------------------------------------------------------------