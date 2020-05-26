from PyQt5 import QtWidgets , QtCore
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QUrl, QDirIterator, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QFileDialog, QAction, QHBoxLayout, QVBoxLayout, QSlider,QMessageBox
from pyqtgraph import PlotWidget, plot, PlotItem
from SongSplitter import Ui_MainWindow
import numpy as np
import pyqtgraph as pg
import sys
import pyaudio
import os
import sounddevice as sd
import warnings
import scipy.io.wavfile as wav
import spleeter.commands.separate
from spleeter.separator import Separator
from scipy.io.wavfile import write
import tensorflow as tf
import librosa
import pandas as pd


tf.get_logger().setLevel('ERROR')
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=Warning)



class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        pg.setConfigOption('background', 'k')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.separator = Separator('spleeter:2stems')
        
        self.Input_X=[]
        self.Input_Y=[]
        self.music=[]
        self.vocals=[]
        

        self.Ecg=[]
        self.Sample_Rate = 1000         #sample rate , taken from the file source 
    #----------------------------------------------------------------------------------------------------------------
        self.graphic_View_Array=[self.ui.Original_GV,self.ui.Vocals_GV,self.ui.Music_GV,self.ui.Original_ECG,self.ui.ECG,self.ui.Arrhythmia]
        for x in self.graphic_View_Array:
            x.getPlotItem().hideAxis('bottom')
            x.getPlotItem().hideAxis('left')
            x.setMouseEnabled(x=False, y=False)

        self.playArray=[self.ui.Play_Music,self.ui.Play_original,self.ui.Play_vocals]
    #----------------------------------------------------------------------------------------------------------------
        self.ui.Import.clicked.connect(self.Import)
        self.ui.Import_ECG.clicked.connect(self.Import_ECG)
    #----------------------------------------------------------------------------------------------------------------'
        self.stopArray=[self.ui.Stop,self.ui.Stop2,self.ui.Stop3]
        for x in self.stopArray:
            x.clicked.connect(self.Stop)
    #----------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------'
        self.ui.Save_music.clicked.connect(lambda: self.Save_music(self.music))
        self.ui.Save_vocals.clicked.connect(lambda: self.Save_vocals(self.vocals))
    #----------------------------------------------------------------------------------------------------------------

    def Import(self):
        filePaths = QtWidgets.QFileDialog.getOpenFileNames(self, 'Multiple File',"~/Desktop",'*')
        for filePath in filePaths:
            for f in filePath: 
                if f == "*" or f == None:
                    break
                ext = os.path.splitext(f)[-1].lower()  # Check file extension  
                if ext == ".wav":
                    self.Input_Y,frame_rate=self.ReadFromWav(f)
                    self.Input_X=np.arange(0,len(self.Input_Y))

                    self.plot(self.Input_X,self.Input_Y[:,0],self.ui.Original_GV,'r')
                    self.ui.Play_original.clicked.connect(lambda : self.Play_Wav(self.Input_Y))

                    self.vocals,self.music=self.split(self.Input_Y)
                    
                    self.plot(self.Input_X[200:len(self.Input_X)-2000],self.music[:,0][200:len(self.Input_X)-2000],self.ui.Music_GV,'w')
                    self.plot(self.Input_X[200:len(self.Input_X)-2000],self.vocals[:,0][200:len(self.Input_X)-2000],self.ui.Vocals_GV,'w')

                    self.ui.Play_Music.clicked.connect(lambda : self.Play_Wav(self.music))
                    self.ui.Play_vocals.clicked.connect(lambda : self.Play_Wav(self.vocals))

                if ext == ".csv":

                    ECG_data= pd.read_csv(f)
                    self.Ecg = [data for data in ECG_data.ECG]
                    self.Ecg = np.array(self.Ecg)
                    x=np.arange(0,len(self.Ecg))
                    self.plot(x,self.Ecg,self.ui.Original_GV,'r')

                    self.split_ECG(self.Ecg)
                    
    def Import_ECG (self):
        filePaths = QtWidgets.QFileDialog.getOpenFileNames(self, 'Multiple File',"~/Desktop",'*')
        for filePath in filePaths:
            for f in filePath: 
                if f == "*" or f == None:
                    break
                ext = os.path.splitext(f)[-1].lower()  # Check file extension  
                if ext == ".csv":
                    ECG_data= pd.read_csv(f)
                    self.Ecg = [data for data in ECG_data.ECG]
                    self.Ecg = np.array(self.Ecg)
                    x=np.arange(0,len(self.Ecg))
                    self.plot(x,self.Ecg,self.ui.Original_ECG,'r')

                    self.split_ECG(self.Ecg)           

      
   #----------------------------------------------------------------------------------------------------------------   

    def ReadFromWav(self,file):
        (freq, sig) = wav.read(file)
        sig=(sig.astype(np.float32))/100000
        return (sig, freq)
        
    #------------------------------------------------------------------------------------------------------------------------ 

    def split_ECG(self,ecg):
        Data, phase = librosa.magphase(librosa.stft(ecg))
        Filter = librosa.decompose.nn_filter(Data,aggregate=np.median,metric='cosine',width=int(librosa.time_to_frames(2, sr=self.Sample_Rate)))
        Filter = np.minimum(Data, Filter)
        margin_i, margin_v = 2, 10
        power = 2
        mask_i = librosa.util.softmask(Filter,margin_i * (Data - Filter),power=power)
        mask_v = librosa.util.softmask(Data - Filter,margin_v * Filter,power=power)

        pure_arrhythmia = (mask_v * Data) * phase
        pure_ECG = (mask_i * Data) * phase
    
        arrhythmia = librosa.istft(pure_arrhythmia)
        ECG = librosa.istft(pure_ECG) * 1.5

        x_A=np.arange(0,len(arrhythmia))
        x_E=np.arange(0,len(ECG))

        # pure ECG
        self.plot(x_E,ECG,self.ui.ECG,'w')
        # Pure arrhythmia
        self.plot(x_A,arrhythmia,self.ui.Arrhythmia,'w')



    def split(self,WavData):
        splitted = self.separator.separate(WavData)
        Music = (splitted.get('accompaniment'))
        Vocals = (splitted.get('vocals'))
        return Vocals,Music


    #------------------------------------------------------------------------------------------------------------------------           
    def Play_Wav(self,array):
        if len(self.Input_Y) != 0:
            sd.play(array)
        else:
            pass
    
    def Stop(self):
        sd.stop()
    #------------------------------------------------------------------------------------------------------------------------
    
    def plot (self,x,y,gv,color):
        gv.clear()
        gv.plotItem.getViewBox().setRange(xRange=x, yRange=y)
        gv.plot(x,y,pen=color)

    #------------------------------------------------------------------------------------------------------------------------
    def Save_music(self,arr):
        if len(self.music)>0:
            write("outputs/music.wav", 44100, arr)
    def Save_vocals(self,arr):
        if len(self.vocals)>0:
            write("outputs/vocals.wav", 44100, arr)
    #------------------------------------------------------------------------------------------------------------------------

#////////////////////////////// Main /////////////////////////////////////

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()

if __name__ == "__main__":
    main()