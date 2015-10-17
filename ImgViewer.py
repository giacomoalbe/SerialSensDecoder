from PyQt4.QtGui import *
from PyQt4.QtCore import *
import png

class ImgRect(QWidget):

	def __init__(self, parent, x_dim, y_dim):

		super(ImgRect, self).__init__()

		self.setParent(parent)
		self.num = [x_dim,y_dim]
		self.lightRange = [40,600]

		# Prendo come base la larghezza della finestra 
		# e la divido per il numero di campioni orizzontali
		self.squareDim = self.width() / self.num[0] 

                self.color = [127 for i in range(x_dim*y_dim)]
		self.center()
        
        def showImage(self, image):
            # Prendiamo i colori dall'immagine 
            # e facciamo il repaint della stessa
            self.color = image
            self.repaint()

	def paintEvent(self, event):

            qp = QPainter()
            qp.begin(self)
            
            count = 0

            for i in range(self.num[0]):
                    for j in range(self.num[1]):
                            
                            color = QColor(self.color[count], self.color[count], self.color[count])

                            qp.setBrush(color)
                            qp.setPen(color)

                            qp.drawRect(i*self.squareDim,j*self.squareDim, self.squareDim, self.squareDim)
                            count = count + 1
                            
            qp.end()

	def center(self):
		self.move(self.parent().frameGeometry().center() - self.frameGeometry().center())
		self.repaint()

	def saveImage(self):

		img_array = []
		img_finale = []

		for color in self.color:

			for i in range(50):
				img_array.append(color.red())
				img_array.append(color.green())
				img_array.append(color.blue())

		print len(img_array) / 3

		rigaTmp = []

		for riga in range(self.num[1]):
			rigaTmp = img_array[riga*self.num[0]*3*50:(riga+1)*self.num[0]*3*50]
			for index in range(50):
				img_finale.append(tuple(rigaTmp))


		fileOut = open('img_saved.png', 'wb')
		writer = png.Writer(50*self.num[0], 50*self.num[1])
		writer.write(fileOut, img_finale)
		fileOut.close()	
	
