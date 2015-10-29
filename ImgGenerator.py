from PyQt4.QtGui import *
from PyQt4.QtCore import *
from random import randint
import numpy as np
import math
from SensDecoder import *
import time

class ImgGenerator():

    """
    Classe che wrappa l'oggetto responsabile
    di creare l'immagine da visualizzare.

    Puo' essere utilizzato come mock per testing
    o in produzione come reale generatore di immagini
    dal sensore o da altra fonte.
    """
    def __init__(self, dim, debug=False):

        # Dimensione dell'immagine, modificabile da costruttore
        self.dim = dim
        self.debug = debug
        self.imageBase = []

        # Range di valori che escono dal sensore fotografico
        # Max Luce LED:     15  ==> 1.0/15  = ~670
        # Min Luce BUIO:    500 ==> 1.0/500 = ~20
        self.lightRange = []

        # Step da utilizzare per la conversione in scala [0,255]
        # per rappresentare l'immagine a livelli di grigio
        #self.step = math.ceil(((self.lightRange[1]-self.lightRange[0]) / 255.00) * 100) / 100.0

        # Init del sensore
        self.initSensore()


    def takeImage(self, period):

        # Cancelliamo il contenuto attuale dell'immagine
        self.image = []

        """
        * Impostiamo il contatore a period
        * Mandiamo il trigger per lo scatto
        * Aspettiamo un tempo pari a period + 5
        * Scarichiamo i dati presenti
        * Inviamo dati immagine
        """

        if self.sensore.setCounter(period):
            # Scatto
            self.sensore.scattaFoto()
            # Aspetto
            time.sleep(period/1000.0)
            # Update del contatore
            self.sensore.getFifoCount()

            # Recupero immagine dal sensore
            # Faccio il cambio di scala
            self.imageBase = self.sensore.getAllValue()
            return self.updateImage()

    def updateImage(self):

        """
        Funzione che si occupa di generare
        i dati per l'immagine e quindi di passarli
        alla MainUI
        """
        if len(self.imageBase) != 0:
            # Comprimiamo l'immagine in base ai lightRange
            imgNorm = self.compressImage(self.imageBase)

            # Genero info sull'immagine
            maxVal = max(imgNorm)
            minVal = min(imgNorm)
            avgVal = (sum(imgNorm) / len(imgNorm))

            # Ritorno info sull'immagine
            return {
                'image'     : imgNorm,
                'imgLen'    : len(imgNorm),
                'maxVal'    : maxVal,
                'minVal'    : minVal,
                'avgVal'    : avgVal
            }

        return None

        
    def generateRandomImage(self):

        """
        Metodo che crea un array di 72 elementi
        con valori tra lighRange
        """
        return self.changeLightScale(
            [randint(self.lightRange[0], self.lightRange[1])
                 for i in range(self.dim)])

    def compressImage(self, img):

        """
        Questa funzione ritorna sempre
        una lista di numeri tra 0 e 100
        dove 0 e' buio totale e 100 e' luce totale
        """
        
        minVal = 1.0/self.lightRange[1]
        maxVal = 1.0/self.lightRange[0]


        imgComprex = []
        val = 0
        
        for elem in img:
            if elem < self.lightRange[0]:
                val = maxVal
            elif elem > self.lightRange[1]:
                val = minVal
            else:
                val = (1.0/elem)

            numerator = (val-minVal)*1e5
            denominator = (maxVal- minVal)*1e5
            newVal = int((numerator/denominator)*255)
            
            imgComprex.append(newVal)

        return imgComprex

    def setLightRange(self, lightRange):
        self.lightRange = lightRange
        
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


