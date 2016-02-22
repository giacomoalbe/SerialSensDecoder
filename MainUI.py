 

from PyQt4 import QtGui
from PyQt4 import QtCore

from math import *
import sys

from ImgGenerator import *
from QHistogram import *
from ImgViewer import *
from StatusBar import *


class MainUI(QtGui.QWidget):

    def __init__(self):

            super(MainUI, self).__init__()

            # Variabile che abilita il testing  anche da riga di comando
            if ('-d' in sys.argv or '--debug' in sys.argv):
                self.debug = True
            else:
                self.debug = False

            # Crea istanza del generatore di immagini
            self.imgGenerator = ImgGenerator(72, self.debug)

            # Indice per tener traccia delle modifiche al comboBox
            self.index = 0
            # Variabile per il loop del realtime
            self.start = False

            # Variabile per init del sensore
            self.isSensorReady = self.imgGenerator.isReady()

            # Inizializza e collega i vari elementi della UI
            self.initUI()

    def initUI(self):

            # MESSAGGI STATUSBAR
            self.messages = {
                'nofoto'        : 'Non e\' presente alcuna foto!',
                'photo'         : 'Foto scattata!',
                'saved'         : 'Immagine salvata!',
                'shooting'      : 'Sto scattando foto...',
                'rifle_done'    : 'Raffica conclusa!',
                'start'         : 'Registrazione Iniziata',
                'stop'          : 'Registrazione Stoppata'
            }

            # MAIN WIDGET
            self.move(10, 300)
            self.setFixedSize(670, 630)
            self.setWindowTitle("SerialSensDecoder")

            # MAIN LAYOUT
            mainLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, self)

            # OTHERS LAYOUT

            ctrlLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight, self)
            statsLayout = QtGui.QGridLayout(self)
            settingsLayout = QtGui.QGridLayout(self)
            buttonsLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight, self)
            bottomLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight, self)


            # WIDGETS
            self.imgViewer = ImgRect(self, 12, 6)
            self.histogram = QHistogram(self, 128)
            self.statusBar = StatusBar(self.messages['nofoto'])

            self.scattaButton = QtGui.QPushButton('Scatta', self)
            self.rtButton = QtGui.QPushButton('Real Time', self)
            self.saveImgButton = QtGui.QPushButton('Salva', self)

            buttonsLayout.addWidget(self.scattaButton)
            buttonsLayout.addWidget(self.rtButton)
            buttonsLayout.addWidget(self.saveImgButton)

            if (self.isSensorReady):
                self.deviceStatus = QtGui.QLabel('Device ready')
                self.deviceStatus.setStyleSheet('color: green; text-align: right')
            else:
                self.deviceStatus = QtGui.QLabel('Device NOT ready')
                self.deviceStatus.setStyleSheet('color: red; text-align: right')
            

            # STATS LABELS

            statsNames = ['_Stats_Image_Raw Image', 'Max', 'Min', 'Average']
            self.statsLabel = {}

            for index, name in enumerate(statsNames):

                # Add the info label

                if name.startswith('_'):
                    # Heading
                    for headIndex, heading in enumerate(name[1:].split('_')):    
                        statsLayout.addWidget(QtGui.QLabel(str(heading)), *[index, headIndex])
                else:

                    # Row name
                    statsLayout.addWidget(QtGui.QLabel(name))
                    
                    self.statsLabel[name] = QtGui.QLabel('0')
                    self.statsLabel['raw' + name] = QtGui.QLabel('0')
                    statsLayout.addWidget(self.statsLabel[name], *[index, 1])
                    statsLayout.addWidget(self.statsLabel['raw' + name], *[index, 2])

            
            self.statsLabel['time'] = QtGui.QLabel('0')
            self.statsLabel['perc'] = QtGui.QLabel('0')
            
            statsLayout.addWidget(QtGui.QLabel('Time'), *[len(statsNames),0])
            statsLayout.addWidget(self.statsLabel['time'], *[len(statsNames),1])
            statsLayout.addWidget(self.statsLabel['perc'], *[len(statsNames),2])
                    
            # SETTINGS LABELS
            self.minRange = (QtGui.QSpinBox(),[1,1]) 
            self.maxRange = (QtGui.QSpinBox(), [2,1])
            self.periodValue = (QtGui.QSpinBox(), [3,1])

            settingTitleLabel = (QtGui.QLabel('SETTINGS'),[0,0])
            minRangeLabel = (QtGui.QLabel('Black'), [1,0])
            maxRangeLabel = (QtGui.QLabel('White'), [2,0])
            periodLabel = (QtGui.QLabel('Period'), [3,0])
            self.minRange[0].setMaximum(1000000)
            self.maxRange[0].setMaximum(1000)
            self.periodValue[0].setMaximum(1200)
            self.periodValue[0].setMinimum(1)

            settingsLayout.addWidget(settingTitleLabel[0], *settingTitleLabel[1])
            settingsLayout.addWidget(minRangeLabel[0], *minRangeLabel[1])
            settingsLayout.addWidget(maxRangeLabel[0], *maxRangeLabel[1])
            settingsLayout.addWidget(periodLabel[0], *periodLabel[1])
            settingsLayout.addWidget(self.minRange[0], *self.minRange[1])
            settingsLayout.addWidget(self.maxRange[0], *self.maxRange[1])
            settingsLayout.addWidget(self.periodValue[0], *self.periodValue[1])
                                    

            ctrlLayout.addLayout(statsLayout)
            ctrlLayout.addLayout(settingsLayout)

            bottomLayout.addWidget(self.statusBar)
            bottomLayout.addWidget(self.deviceStatus) 

            mainLayout.addWidget(self.imgViewer)
            mainLayout.addWidget(self.histogram)
            mainLayout.addLayout(ctrlLayout)
            mainLayout.addLayout(buttonsLayout)
            mainLayout.addLayout(bottomLayout)

            self.setLayout(mainLayout)

            # Timer per il RT delle foto
            self.timerRt = QTimer()

            self.minRange[0].setValue(5000)
            self.maxRange[0].setValue(400)
            self.periodValue[0].setValue(400)
            self.rangeChanged()
            self.show()

            # EVENTS

            self.scattaButton.clicked.connect(self.shootImage)
            #saveImgBtn.clicked.connect(self.saveImage)
            self.rtButton.clicked.connect(self.realTime)
            #self.saveImgButton.clicked.connect(self.saveImages)

            # LIGHT RANGE CHANGES
            self.minRange[0].valueChanged.connect(self.rangeChanged)
            self.maxRange[0].valueChanged.connect(self.rangeChanged)
            #self.periodValue[0].valueChanged.connect(self.periodChanged)

            # Agganciamo l'evento timeout()
            # all'evento scatta foto
            self.timerRt.timeout.connect(self.shootImage)

    def shootImage(self):

        if (self.isSensorReady):

            self.paintImage(self.imgGenerator.takeImage(self.periodValue[0].value()))
            
            
    def rangeChanged(self, val=0):

        """
        Cambiamo i valori di max e min
        e quindi facciamo il refresh della compressione
        """

        self.imgGenerator.setLightRange([self.maxRange[0].value(),
                                         self.minRange[0].value()])
        self.paintImage(self.imgGenerator.updateImage())

    def realTime(self):

        if self.start == True:
            # Stoppiamo il realtime sull'ultima foto
            # e rimettiamo il label corretto
            self.timerRt.stop()
            self.start = False
            self.rtButton.setText('Start')
            self.statusBar.changeMessage(self.messages['stop'])
        else:
            self.timerRt.start((self.periodValue[0].value() + 10) / 1000.0)
            self.start = True
            # Cambianmo la label dello scattaButton
            self.rtButton.setText('Stop')
            self.statusBar.changeMessage(self.messages['start'])
        

    def paintImage(self, imageInfo):

        if imageInfo is not None:
            self.imgViewer.showImage(imageInfo['image'])
            self.histogram.showImage(imageInfo['image'])

            perc = imageInfo['time'] / float(self.periodValue[0].value()*1000)

            # Update Image Stats
            for field in ['Max', 'Min', 'Average']:
                self.statsLabel[field].setText("%d" % (imageInfo[field]))
                self.statsLabel['raw' + field].setText("%d" % (imageInfo['raw' + field]))
                
            self.statsLabel['time'].setText("{0:d} us".format(imageInfo['time']))
            self.statsLabel['perc'].setText("{0:.2%}".format(perc))

        
    def saveImage(self):

            self.imgViewer.saveImage(self.changeStatusBar)

    def changeStatusBar(self):

            self.statusBar.changeMessage(self.messages['saved'])

