#!/usr/bin/python
# -*- coding: utf-8 -*-

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
            # Crea istanza del generatore di immagini	
            self.imgGenerator = ImgGenerator(72)
            # Inizializza e collega i vari elementi della UI
            self.initUI()
            # Variabile che abilita il testing
            self.debug = True

	def initUI(self):
            

            # MESSAGGI STATUSBAR
            self.messages = {
                'nofoto' : 'Non e\' presente alcuna foto!',
                'photo'  : 'Foto scattata!',
                'saved'  : 'Immagine salvata!'
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

            # WIDGETS
            self.imgViewer = ImgRect(self, 12, 6)
            self.histogram = QHistogram(128)
            self.statusBar = StatusBar(self.messages['nofoto'])

            scattaButton = QtGui.QPushButton('Shoot Image', self)
            saveImgBtn = QtGui.QPushButton('Save Image', self)
            statsImgBtn = QtGui.QPushButton('View Stats', self)

            modeCombo	= QtGui.QComboBox(self) 
            lightCombo 	= QtGui.QComboBox(self)

            modeCombo.addItem('Single')
            modeCombo.addItem('Rifle')

            lightCombo.addItem('high')
            lightCombo.addItem('middle')
            lightCombo.addItem('low')

            # Imposta i Layout della Immagine
            comboTopLayout.addWidget(modeCombo)
            comboTopLayout.addWidget(lightCombo)
            comboTopLayout.addWidget(scattaButton)
            comboTopLayout.addWidget(saveImgBtn)
            comboTopLayout.addWidget(statsImgBtn)

            bottomLayout.addWidget(self.histogram)
            bottomLayout.addLayout(comboTopLayout)
            bottomLayout.addWidget(self.statusBar)
            
            mainLayout.addWidget(self.imgViewer)
            mainLayout.addLayout(bottomLayout)

            self.setLayout(mainLayout)

            self.show()

            # EVENTS

            scattaButton.clicked.connect(self.generateNewImage)
            saveImgBtn.clicked.connect(self.saveImage)


        def generateNewImage(self):

            """ 
            Funzione che genera una nuova immagine
            mappa il suo contenuto all'interno di 0,256
            fa update su imgViewer
            fa update su histogram
            """
            
            image = self.imgGenerator.takeImage(self.debug)
            self.imgViewer.showImage(image)
            self.histogram.showImage(image)

            self.statusBar.changeMessage(self.messages['photo'])
    
        def saveImage(self):
                
            self.imgViewer.saveImage(self.changeStatusBar)

        def changeStatusBar(self):

            self.statusBar.changeMessage(self.messages['saved'])
