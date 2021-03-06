from PyQt4.QtGui import *
from PyQt4.QtCore import *
import numpy
from random import randint

class QHistogram(QWidget):

    """
    Widget che mostra l'istogramma di una immagine usando
    un range di 256 livelli da nero totale a bianco totale
    """

    def __init__(self, parent, bins):

        super(QHistogram, self).__init__()
        self.binNum = bins
        self.setParent(parent)
        
        # Dati dell'immagine (inizialmente tutti 0)
        self.image = []

        # Imposta altezza a 120
        self.setMinimumHeight(120)
        self.setMaximumHeight(120)

    def paintEvent(self, event):

        # Istogramma dei bin
        istogram = numpy.histogram(self.image, bins = range(self.binNum+1))[0]
        
        # Normalizzo istogramma
        sumHist = float(sum(istogram))
        normHist = [(x/sumHist) for x in istogram]

        qp = QPainter()
        qp.begin(self)

        # Rettangolo Bianco di Sfondo
        qp.setPen(QColor(255,255,255, 255))
        qp.setBrush(QColor(255,255,255,255))
        qp.drawRect(0,0,self.width(),90)

        self.binWidth = self.width() / float(self.binNum)
        
        refHeight = 2.0 * max(normHist)

        for i in range(len(normHist)):

            greyShade = int(i / 0.5)
            color = QColor(greyShade,greyShade,greyShade, 255)

            qp.setPen(color)
            qp.setBrush(color)

            x = i * (self.binWidth)
            y = 80

            if numpy.isnan(normHist[i]):
                height = 0
            else:
                height = -(90 * normHist[i] / refHeight)

            qp.drawRect(x,y,self.binWidth, height)
            qp.drawRect(x, 100, self.binWidth, -20)
        qp.end()

    def showImage(self, image):

        if image == None:
            return
        self.image = image
        self.repaint()

        imgInfo = []
        imgInfo.append(max(image))
        imgInfo.append(min(image))
        imgInfo.append(sum(image) / len(image))

        return imgInfo
