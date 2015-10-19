from PyQt4.QtGui import *
from PyQt4.QtCore import *


class StatusBar(QWidget):

    def __init__(self, message):
        super(StatusBar, self).__init__()
        self.message = message
        self.setGeometry(0,self.width() - 30, self.width(), 30)
        self.setMaximumHeight(20)

    def changeMessage(self, message):
        self.message = message
        self.repaint()

    def paintEvent(self, event):
        
        qp = QPainter()
        qp.begin(self)
    
        qp.setBrush(QColor(255,255,255,255))
        qp.setPen(QColor(0,0,0,255))
        qp.drawText(event.rect(), Qt.AlignLeft, self.message)
        qp.end()

