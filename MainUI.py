

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
            self.setFixedSize(670, 570)
            self.setWindowTitle("SerialSensDecoder")

            # MAIN LAYOUT
            mainLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, self)

            # OTHERS LAYOUT
            comboTopLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight, self)
            bottomLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, self)
            imgInfoLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight, self)

            # WIDGETS
            self.imgViewer = ImgRect(self, 12, 6)
            self.histogram = QHistogram(128)
            self.statusBar = StatusBar(self.messages['nofoto'])

            self.scattaButton = QtGui.QPushButton('Scatta', self)
            saveImgBtn = QtGui.QPushButton('Salva', self)
            statsImgBtn = QtGui.QPushButton('Stats', self)

            # INFO LABELS
            self.maxValue = QtGui.QLabel('Max: ')
            self.minValue = QtGui.QLabel('Min: ')
            self.averageValue = QtGui.QLabel('Average: ')

            imgInfoLayout.addWidget(self.maxValue)
            imgInfoLayout.addWidget(self.minValue)
            imgInfoLayout.addWidget(self.averageValue)

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

            bottomLayout.addLayout(imgInfoLayout)
            bottomLayout.addWidget(self.histogram)
            bottomLayout.addLayout(comboTopLayout)
            bottomLayout.addWidget(self.statusBar)

            mainLayout.addWidget(self.imgViewer)
            mainLayout.addLayout(bottomLayout)

            self.setLayout(mainLayout)

            # Timer per il RT delle foto
            self.timerRt = QTimer()


            self.show()

            # EVENTS

            self.scattaButton.clicked.connect(self.generateNewImage)
            saveImgBtn.clicked.connect(self.saveImage)
            modeCombo.activated[int].connect(self.comboChanged)

            # Agganciamo l'evento timeout()
            # all'evento scatta foto
            self.timerRt.timeout.connect(self.shootSingleImage)

    def generateNewImage(self):

            """
            Funzione che smista le operazioni:
            1. Se self.index == 0 ==> scatta una immagine
            2. Se self.index == 1 ==> scatta 1000 immagini e le salva
            3. se self.index == 2 ==> fa il realtime dalla fotocamera
            """

            if (self.index == 0):

                self.shootSingleImage()
                self.statusBar.changeMessage(self.messages['photo'])

            elif (self.index == 1):

                # TODO scatta 1000 foto
                # Scattiamo 1000 foto e quindi le salviamo
                # su un file di testo nella cartella, con indicazione temporale
                self.statusBar.changeMessage(self.messages['shooting'])
                self.imgGenerator.takeRiflePhoto()
                self.statusBar.changeMessage(self.messages['rifle_done'])
            else:
                if self.start == True:
                    # Stoppiamo il realtime sull'ultima foto
                    # e rimettiamo il label corretto
                    self.timerRt.stop()
                    self.start = False
                    self.scattaButton.setText('Start')
                    self.statusBar.changeMessage(self.messages['stop'])
                else:
                    self.timerRt.start(int(1.0/30.0))
                    self.start = True
                    # Cambianmo la label dello scattaButton
                    self.scattaButton.setText('Stop')
                    self.statusBar.changeMessage(self.messages['start'])

    def shootSingleImage(self):

            image = self.imgGenerator.takeImage()
            self.imgViewer.showImage(image)
            imageInfo = self.histogram.showImage(image)

            # Update Image info
            self.maxValue.setText('Max: %d' % imageInfo[0])
            self.minValue.setText('Min: %d' % imageInfo[1])
            self.averageValue.setText('Average: %d' % imageInfo[2])

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

