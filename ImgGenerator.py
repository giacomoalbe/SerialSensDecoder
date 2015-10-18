from PyQt4.QtGui import *
from PyQt4.QtCore import *
from random import randint
import numpy as np
import math 

class ImgGenerator():
    """
    Classe che wrappa l'oggetto responsabile
    di creare l'immagine da visualizzare.

    Puo' essere utilizzato come mock per testing
    o in produzione come reale generatore di immagini 
    dal sensore o da altra fonte.
    """
    def __init__(self, dim):
        
        # Dimensione dell'immagine, modificabile da costruttore
        self.dim = dim
        self.image = []

        # Range di valori che escono dal sensore fotografico
        self.lightRange = [16,250]

        # Step da utilizzare per la conversione in scala [0,255] 
        # per rappresentare l'immagine a livelli di grigio
        self.step = math.ceil(((self.lightRange[1]-self.lightRange[0]) / 255.00) * 100) / 100.0
    
    def takeImage(self, mock=False):

        # Cancelliamo il contenuto attuale dell'immagine
        self.image = []
        
        if mock:
            # Creiamo una immagine casuale, per testing
            self.image = self.generateRandomImage()        
            return self.image

        # TODO:
        # ritornare immagine generata dal sensore
        # return SensImage()

    def generateRandomImage(self):
        
        """
        Metodo che crea un array di 72 elementi 
        con valori tra 40 e 600 e li mappa su un array di 256 elementi
        """
        image = []

        for i in range(self.dim):
            # Genera valore casuale
            value = randint(self.lightRange[0], self.lightRange[1])
            # Trasforma il valore nella nuova scala [0,255]
            newValue = int((value - self.lightRange[0]) / self.step)    
            # Inserisce il valore del pixel nell'immagine
            image.append(newValue)

        return image 

             

