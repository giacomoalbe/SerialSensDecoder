from PyQt4.QtGui import *
from PyQt4.QtCore import *
import png

import time

class ImgRect(QWidget):

	def __init__(self, parent, x_dim, y_dim):

		super(ImgRect, self).__init__()

		self.setParent(parent)
		self.num = [x_dim,y_dim]
		self.lightRange = [40,600]

		# Prendo come base la larghezza della finestra 
		# e la divido per il numero di campioni orizzontali
		self.squareDim = self.width() / self.num[0] 
                
                # Init dell'array immagine con valori fissi
                self.color = [127 for i in range(x_dim*y_dim)]
                # Numero di immagini salvate
                self.imageSaved = 0
        
        def showImage(self, image):
            # Prendiamo i colori dall'immagine 
            # e facciamo il repaint della stessa
            if image == None:
                    return
            self.color = image
            self.repaint()

	def paintEvent(self, event):

            qp = QPainter()
            qp.begin(self)
            
            count = 0
            
            # Per ogni riga scrivo le colonne
            for row in range(self.num[1]):
                for col in range(self.num[0]):
                    # Genariamo il colore a partire dal valore nel conteggio        
                    color = QColor(self.color[count], self.color[count], self.color[count])
                    # Coloriamo opportunamente la penna e il pennello
                    qp.setBrush(color)
                    qp.setPen(color)
                    # Disegnamo il valore di altezza del pixel nell'istogramma
                    qp.drawRect(col*self.squareDim,row*self.squareDim, self.squareDim, self.squareDim)
                    # Aggiorniamo il conteggio dei pixel
                    count = count + 1
                            
            qp.end()

	def saveImage(self, callback):

		img_array = []
		img_finale = []
                
                # Aggiungiamo 50 volte la terna (BW) per creare un pixel
		for color in self.color:
                    for i in range(50):
                        img_array.append(color)
                        img_array.append(color)
                        img_array.append(color)

		rigaTmp = []
                
                # Inseriamo un numero di righe pari al valore delle righe dell'immagine
		for riga in range(self.num[1]):
                    rigaTmp = img_array[riga*self.num[0]*3*50:(riga+1)*self.num[0]*3*50]
                    for index in range(50):
                        img_finale.append(tuple(rigaTmp))
                
                # Assegnamo un nome univoco (basato sul tempo) ad ogni foto
                nomeFile = 'img/' + str(int(time.time()*1000000)) + '_' + str(self.imageSaved) + ".png"
                # Aumentiamo il contatore delle immagini salvate
                self.imageSaved = self.imageSaved + 1

		fileOut = open(nomeFile, 'wb')
		writer = png.Writer(50*self.num[0], 50*self.num[1])
		writer.write(fileOut, img_finale)
		fileOut.close()	
                
                # Quando finisce l'esecuzione eseguiamo la funzione di callback
                callback()
	
