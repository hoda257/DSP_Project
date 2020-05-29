from designImage import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
import sys
import os
import pyqtgraph as pg
import numpy as np 
from PIL import Image
import cv2



class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        pg.setConfigOption('background', 'w')
        self.ui =  Ui_MainWindow()
        self.ui.setupUi(self)
        #----------------------------------------------------------------------------------------------------------------------
        #----------------------------------------------------------------------------------------------------------------------
        self.outputPaths = [ "outputs/Output1.jpeg" , "outputs/Output2.jpeg" , "outputs/Output3.jpeg","outputs/Output4.jpeg" , "outputs/Output5.jpeg" , "outputs/Output6.jpeg","outputs/Output7.jpeg", "outputs/Output8.jpeg"]
        self.ui.browseImage.clicked.connect(self.Browse)
        self.images = [self.ui.Image1, self.ui.Image2, self.ui.Image3, self.ui.Image4, self.ui.Image5, self.ui.Image6,
        self.ui.Image7, self.ui.Image8]
        for x in self.images:
            x.getPlotItem().hideAxis('bottom')
            x.getPlotItem().hideAxis('left')
            x.setMouseEnabled(x=False, y=False)
        #----------------------------------------------------------------------------------------------------------------------
        #----------------------------------------------------------------------------------------------------------------------
        self.startingIndexes=[]
        self.jpegData=[]

#----------------------------------------------------------------------------------------------------------------------
  #//////////////////////////// Browse ///////////////////////////
    def Browse (self):
            fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", "Desktop", '*.jpg *.jpeg')
            if fname:
                self.ReadImageHexadecimal(fname)
                self.GetIndexes('ffda')

                if len(self.startingIndexes)<=7:
                   QMessageBox.warning(self,'Warning',"LOW QUALITY IMAGE :)", QMessageBox.Ok )

                elif len(self.startingIndexes)==8:
                    for i in range(7):
                        JpegByteData=open(fname , "rb").read(self.startingIndexes[i+1])
                        OutputData = open('outputs/Output'+str(i+1)+'.jpeg',"wb")
                        OutputData.write(JpegByteData)
                        OutputData.write(b'\xff\xd9')
                        OutputData.close()
                        img=cv2.imread(self.outputPaths[i])
                        self.plot(self.images[i],cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

                    self.plot(self.images[-1],cv2.cvtColor(cv2.imread(fname), cv2.COLOR_BGR2RGB))
                    JpegByteData=open(fname , "rb").read(self.startingIndexes[-1])
                    OutputData = open('outputs/Output8.jpeg',"wb")
                    OutputData.write(JpegByteData)
                    OutputData.write(b'\xff\xd9')
                    OutputData.close()

                elif len(self.startingIndexes)>8:
                    for i in range(8):
                        JpegByteData=open(fname , "rb").read(self.startingIndexes[i+1])
                        OutputData = open('outputs/Output'+str(i+1)+'.jpeg',"wb")
                        OutputData.write(JpegByteData)
                        OutputData.write(b'\xff\xd9')
                        OutputData.close()
                        
                        img=cv2.imread(self.outputPaths[i])
                        self.plot(self.images[i],cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                        
#----------------------------------------------------------------------------------------------------------------------

#///////////////////////// Plot /////////////////////////////////////////////
    def plot(self,graph,Item): 
        PlottedItem = pg.ImageItem(np.asarray(Item))
        graph.clear()
        graph.addItem(PlottedItem)
        PlottedItem.rotate(270) 

#----------------------------------------------------------------------------------------------------------------------

#//////////////////////// Read image data with hexadecimal /////////////////
    def ReadImageHexadecimal(self,filePath):
        self.jpegData = open(filePath,'rb').read().hex()
        self.jpegData = list(map(''.join, zip(self.jpegData[::2], self.jpegData[1::2])))
        
#----------------------------------------------------------------------------------------------------------------------

#//////////////////////// get Indexes of ffda columns //////////////////////

    def GetIndexes(self,starting_byte):                            #- kol image byb2a feha columns hya elly e7na han2sm el image le 8 menha , w ne2ra el data mn awl col l7d el tany w b3den mn el awl l7d el talt w kea 
        if len(self.jpegData)!=0:                                            #  fa hwa 3shan ngeb el index bta3 awl kol column , mn wikipedia 3rft eno awl kol column byb2a "0xff 0xda" w fe el function elly fo2 shelna el 0x menhom
            self.startingIndexes=[]                      
            for i in range (len(self.jpegData)-1):
                if (starting_byte == self.jpegData[i] + self.jpegData[i+1]):
                    self.startingIndexes.append(i)
        else:
            pass
#----------------------------------------------------------------------------------------------------------------------



# ///////////////////////////////////// Main ////////////////////////////////////
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()

#----------------------------------------------------------------------------------------------------------------------
