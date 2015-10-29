

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
            self.isSensorReady = True

            # Tempo di apertura del trigger per l'immagine
            self.currentPeriod = 1200

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
            self.setFixedSize(670, 600)
            self.setWindowTitle("SerialSensDecoder")

            # MAIN LAYOUT
            mainLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, self)

            # OTHERS LAYOUT
            comboTopLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight, self)
            bottomLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, self)
            imgInfoLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight, self)
            lightRangeLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight, self)
            topInfoLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, self)

            # WIDGETS
            self.imgViewer = ImgRect(self, 12, 6)
            self.histogram = QHistogram(self, 128)
            self.statusBar = StatusBar(self.messages['nofoto'])

            self.scattaButton = QtGui.QPushButton('Scatta', self)
            saveImgBtn = QtGui.QPushButton('Salva', self)
            statsImgBtn = QtGui.QPushButton('Stats', self)

            # INFO LABELS
            self.maxValue = QtGui.QLabel('Max: ')
            self.minValue = QtGui.QLabel('Min: ')
            self.averageValue = QtGui.QLabel('Average: ')

            # MAX MIN SPIN BOXES
            self.minRange = QtGui.QSpinBox()
            self.maxRange = QtGui.QSpinBox()

            minRangeLabel = QtGui.QLabel('Min Threshold')
            maxRangeLabel = QtGui.QLabel('Max Threshold')

            self.minRange.setMaximum(1000000)
            self.maxRange.setMaximum(1000)

            self.fpsLabel = QtGui.QLabel('fps: 00')
            self.fpsLabel.setStyleSheet('color: green')

            self.periodValue = QtGui.QSpinBox()
            

            lightRangeLayout.addWidget(minRangeLabel)
            lightRangeLayout.addWidget(self.minRange)   
            lightRangeLayout.addWidget(maxRangeLabel)
            lightRangeLayout.addWidget(self.maxRange)
            
            imgInfoLayout.addWidget(self.maxValue)
            imgInfoLayout.addWidget(self.minValue)
            imgInfoLayout.addWidget(self.averageValue)
            imgInfoLayout.addWidget(self.fpsLabel)
            imgInfoLayout.addWidget(self.periodValue)

            modeCombo   = QtGui.QComboBox(self)
            lightCombo  = QtGui.QComboBox(self)
            modeCombo.addItem('Single')
            modeCombo.addItem('Rifle')
            modeCombo.addItem('Real-time')

            lightCombo.addItem('high')
            lightCombo.addItem('middle')
            lightCombo.addItem('low')

            # Imposta i Layout della Immagine
            comboTopLayout.addWidget(modeCombo)
            comboTopLayout.addWidget(lightCombo)
            comboTopLayout.addWidget(self.scattaButton)
            comboTopLayout.addWidget(saveImgBtn)
            comboTopLayout.addWidget(statsImgBtn)

            topInfoLayout.addLayout(imgInfoLayout)
            topInfoLayout.addLayout(lightRangeLayout)
            
            bottomLayout.addLayout(topInfoLayout)
            bottomLayout.addWidget(self.histogram)
            bottomLayout.addLayout(comboTopLayout)
            bottomLayout.addWidget(self.statusBar)

            mainLayout.addWidget(self.imgViewer)
            mainLayout.addLayout(bottomLayout)

            self.setLayout(mainLayout)

            # Timer per il RT delle foto
            self.timerRt = QTimer()

            self.minRange.setValue(1e6)
            self.maxRange.setValue(1e1)
            self.rangeChanged()
            self.show()

            # EVENTS

            self.scattaButton.clicked.connect(self.generateNewImage)
            saveImgBtn.clicked.connect(self.saveImage)
            modeCombo.activated[int].connect(self.comboChanged)

            # LIGHT RANGE CHANGES
            self.minRange.valueChanged.connect(self.rangeChanged)
            self.maxRange.valueChanged.connect(self.rangeChanged)
            self.periodValue.valueChanged.connect(self.periodChanged)

            # Agganciamo l'evento timeout()
            # all'evento scatta foto
            self.timerRt.timeout.connect(self.handleShoot)
            
    def rangeChanged(self, val=0):

        """
        Cambiamo i valori di max e min
        e quindi facciamo il refresh della compressione
        """

        self.imgGenerator.setLightRange([self.maxRange.value(),
                                         self.minRange.value()])
        self.paintImage(self.imgGenerator.updateImage())
        
    def periodChanged(self, val):

        print "Period changed to %d" % val
    def generateNewImage(self):

            """
            Funzione che smista le operazioni:
            1. Se self.index == 0 ==> scatta una immagine
            2. Se self.index == 1 ==> scatta 1000 immagini e le salva
            3. se self.index == 2 ==> fa il realtime dalla fotocamera
            """

            if (self.index == 0):
                
                self.handleShoot()
                self.statusBar.changeMessage(self.messages['photo'])

            elif (self.index == 1):
                
                # TODO scatta 1000 foto
                # Scattiamo 1000 foto e quindi le salviamo
                # su un file di testo nella cartella, con indicazione temporale
                # self.statusBar.changeMessage(self.messages['shooting'])
                # self.imgGenerator.takeRiflePhoto()
                # self.statusBar.changeMessage(self.messages['rifle_done'])
                pass
            else:
                if self.start == True:
                    # Stoppiamo il realtime sull'ultima foto
                    # e rimettiamo il label corretto
                    self.timerRt.stop()
                    self.start = False
                    self.scattaButton.setText('Start')
                    self.statusBar.changeMessage(self.messages['stop'])
                else:
                    self.timerRt.start((self.currentPeriod + 10) / 1000.0)
                    self.start = True
                    # Cambianmo la label dello scattaButton
                    self.scattaButton.setText('Stop')
                    self.statusBar.changeMessage(self.messages['start'])

    def handleShoot(self):

        """
        NEW MODE:
        attiva trigger del sensore
        aspetta periodo + 10
        scarica il numero di dati presenti
        gli altri li colora di rosso
        """
        imageInfo = self.imgGenerator.takeImage(self.currentPeriod)

        """
        print imageInfo['imgLen']
        print len(imageInfo['image'])

        print "=================="
        print "      Stats       "
        print "=================="
        print
        print "Info"
        print "------------------"
        print "Max: %d\nMin: %d\nAvg: %d\n" % (imageInfo['maxVal'],
                                           imageInfo['minVal'],
                                           imageInfo['avgVal'])
        print "------------------"
        print "Image"
        print "------------------"
        stringa = ""
        for i in range(imageInfo['imgLen']):
            stringa += "%d\t%d\n" % (i,
                                     imageInfo['image'][i])
        print stringa
        print "------------------"
        """
        self.paintImage(imageInfo)
        

    def paintImage(self, imageInfo):

        if imageInfo is not None:
            self.imgViewer.showImage(imageInfo['image'])
            self.histogram.showImage(imageInfo['image'])

            # Update Image info
            self.setFpsLabel(imageInfo['imgLen'])
            self.maxValue.setText('Max: %d' % imageInfo['maxVal'])
            self.minValue.setText('Min: %d' % imageInfo['minVal'])
            self.averageValue.setText('Average: %d' % imageInfo['avgVal'])
        
    def setFpsLabel(self, imgLen):
        # TODO
        # Cambiare la label a seconda che la velocita'
        # permetta o meno di riprendere tutti i pixel
        pass
        
    def saveImage(self):

            self.imgViewer.saveImage(self.changeStatusBar)

    def changeStatusBar(self):

            self.statusBar.changeMessage(self.messages['saved'])

    def comboChanged(self, index):

            # Update del index del combo
            self.index = index;

            if (index == 2):
                # Modifichiamo il label di scattaButton
                self.scattaButton.setText('Start')
            else:
                self.scattaButton.setText('Scatta')

