#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore

from math import *
import sys

from ImgGenerator import * 
from QHistogram import *
from ImgViewer import *


class MainUI(QtGui.QWidget):

	def __init__(self):

		super(MainUI, self).__init__()
		
                self.imgGenerator = ImgGenerator()
		self.initUI()

	def initUI(self):

		# MAIN WIDGET
                self.move(10, 300)
		self.setFixedSize(680, 540)
		self.setWindowTitle("SerialSensDecoder")

		# MAIN LAYOUT
		mainLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, self)

		# OTHERS LAYOUT
		comboTopLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight, self)
                bottomLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, self)

		# WIDGETS
		self.imgViewer = ImgRect(self, 12, 6)
		self.histogram = QHistogram(128)

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


		comboTopLayout.addWidget(modeCombo)
		comboTopLayout.addWidget(lightCombo)
		comboTopLayout.addWidget(scattaButton)
		comboTopLayout.addWidget(saveImgBtn)
		comboTopLayout.addWidget(statsImgBtn)

                self.histogram.setMaximumHeight(120)
                bottomLayout.addWidget(self.histogram)
                bottomLayout.addLayout(comboTopLayout)
                
		mainLayout.addWidget(self.imgViewer)
                mainLayout.addLayout(bottomLayout)

		self.setLayout(mainLayout)

		self.show()

		# EVENTS

		scattaButton.clicked.connect(self.generateNewImage)
		saveImgBtn.clicked.connect(self.imgViewer.saveImage)


        def generateNewImage(self):

            """ 
            Funzione che genera una nuova immagine
            mappa il suo contenuto all'interno di 0,256
            fa update su imgViewer
            fa update su histogram
            """
            
            image = self.imgGenerator.generateImage()
            self.imgViewer.showImage(image)
            self.histogram.showImage(image)

	def center(self):

		contextCenter = QtGui.QDesktopWidget().availableGeometry().center()
		selfContext = self.frameGeometry()
		selfContext.moveCenter(contextCenter)
		self.move(selfContext.topLeft())

