from PyQt4.QtGui import *
from PyQt4.QtCore import *
from random import randint
import numpy as np
import math
#from SensDecoder import *

class ImgGenerator():

    """
    Classe che wrappa l'oggetto responsabile
    di creare l'immagine da visualizzare.

    Puo' essere utilizzato come mock per testing
    o in produzione come reale generatore di immagini
    dal sensore o da altra fonte.
    """
    def __init__(self, dim, debug):

        # Dimensione dell'immagine, modificabile da costruttore
        self.dim = dim
        self.debug = debug
        self.image = []

        # Range di valori che escono dal sensore fotografico
        # Max Luce LED:     15  ==> 1.0/15  = ~670
        # Min Luce BUIO:    500 ==> 1.0/500 = ~20
        self.lightRange = [20,670]

        # Step da utilizzare per la conversione in scala [0,255]
        # per rappresentare l'immagine a livelli di grigio
        self.step = math.ceil(((self.lightRange[1]-self.lightRange[0]) / 255.00) * 100) / 100.0

        # Init del sensore
        # self.initSensore()


    def takeImage(self):

        # Cancelliamo il contenuto attuale dell'immagine
        self.image = []

        if self.debug:
            # Creiamo una immagine casuale, per testing
            self.image = self.generateRandomImage()
            return self.image

        # Ritorna l'immagine generata dal sensore
        self.image = self.changeLightScale(self.sensore.scattaFoto())
        return self.image


    def generateRandomImage(self):

        """
        Metodo che crea un array di 72 elementi
        con valori tra lighRange
        """
        return self.changeLightScale(
            [randint(self.lightRange[0], self.lightRange[1])
                 for i in range(self.dim)])

    def changeLightScale(self, img_array):
        """
        Funzione che trasforma il segnale
        da lightRange a 0...255
        """
        image = []

        for pixel in img_array:
            # Trasforma il valore nella nuova scala [0,255]
            newValue = int((pixel - self.lightRange[0]) / self.step)
            # Inserisce il valore del pixel nell'immagine
            image.append(newValue if newValue < 255 else 255)

        return image

    def initSensore(self):

        # Creo una istanza del sensore
        self.sensore = SensDecoder()
    """
    ==========
    RIFLE MODE
    ==========
    """
    def takeRiflePhoto(self, number=10):

        fileOut = open('./log/prova.dat', 'a')

        for i in range(number):
            # Scattiamo una foto!
            # TODO: set self.debug from parent widget
            image = self.takeImage()
            for index in range(len(image)):
                fileOut.write(str(image[index]))
                if (index != len(image)-1):
                    fileOut.write(",")
            fileOut.write(";\n")
        fileOut.write(72*"="+"\n")
        fileOut.close()

    """
    ====================
    REAL TIME RECORDING
    ====================
    """
    def startRt(self):

        self.timerRt.start(1000)

    def stopRt(self):

        self.timerRt.stop()

