from PyQt4.QtGui import *
from PyQt4.QtCore import *
from random import randint
import numpy as np
import math 

class ImgGenerator():

    def __init__(self):

        self.dim = 72
        self.image = []
        self.lightRange = [16,250]
        self.step = math.ceil(((self.lightRange[1]-self.lightRange[0]) / 255.00) * 100) / 100.0

    def generateImage(self):

        """
        Metodo che crea un array di 72 elementi 
        con valori tra 40 e 600 e li mappa su un array di 256 elementi
        """
        self.image = [] 
        image = []

        for i in range(self.dim):
            value = randint(self.lightRange[0], self.lightRange[1])
            newValue = int((value - self.lightRange[0]) / self.step)
            self.image.append(newValue)

        return self.image 

             

