"""
Funzioni per settare velocemente frequenza di campionamento
e ricevere i dati dal sensore
"""

import ok
import time

trigIn = [
    0x40,   # Port
    0x00,   # Start photo
    0x01,   # Set the counter from WireIns
    0x02    # Restore the downAck
]

wireIn = [
    0x03    # Port
]

wireOut = [
    0x20,   # Port - downAck
    0x21    # Port - fifoCount
]

pipeOut = [
    0xA0,   # Port - Fifo A
    0xA1    # Port - Fifo B
]

class Xem:

    def __init__(self):

        self.xem = ok.FrontPanel()
        self.xem.OpenBySerial("")
        self.xem.ConfigureFPGA('../../sensore.bit')
        self.count = 0
        self.values = []

    def setCounter(self, period):

        """
        Set the period of the trigger for taking a photo
        period is in milliseconds
        """
        if (period <= 1200) and (period >= 1):
            self.xem.SetWireInValue(wireIn[0], period)
            self.xem.UpdateWireIns()
            self.xem.ActivateTriggerIn(trigIn[0], trigIn[2])
            return True
        return False

    def startTrigger(self):
        self.xem.ActivateTriggerIn(trigIn[0], trigIn[1])

    def checkForPhoto(self):

        self.xem.UpdateWireOuts()

        if self.xem.GetWireOutValue(wireOut[0]) == 1:
            # Able to download all the values
            # TODO: downalod

            # Unflag the downAck
            self.xem.ActivateTriggerIn(trigIn[0], trigIn[2])
            return True
        # Unable to download the files
        return False

    def getFifoCount(self):

        self.xem.UpdateWireOuts()
        self.count = self.xem.GetWireOutValue(wireOut[1])
        return self.count

    def takePhotos(self, period):

        self.setCounter(period)

        while True:
            self.startTrigger()
            time.sleep((period + 10) / 1000.0)
            if self.checkForPhoto():
                print "Foto scattata!"
            else:
                print "Foto NON scattata!"

    def getAllValue(self):

        if self.count > 0:

            wordA = '00' * self.count
            wordB = '00' * self.count

            self.xem.ReadFromPipeOut(pipeOut[0], wordA)
            self.xem.ReadFromPipeOut(pipeOut[1], wordB)

            for row in range(1,self.count):

                newValue = ''.join((format(ord(wordA[2*row+1]), '08b'),
                                   format(ord(wordA[2*row]), '08b'), 
                                   format(ord(wordB[2*row+1]), '08b'),
                                   format(ord(wordB[2*row]), '08b')))
                self.values.append(int(newValue,2))

            maxVal = max(self.values)
            minVal = min(self.values)
            avgVal = (sum(self.values) / len(self.values))
            
            return {
                'image'     : self.values,
                'imgLen'    : self.count,
                'maxVal'    : maxVal,
                'minVal'    : minVal,
                'avgVal'    : avgVal
            }
                
            
    def shootPhoto(self, period):

        if self.setCounter(period):

            self.startTrigger()
            time.sleep((period+10) / 1000.0)
            if self.getFifoCount() == 73:
                self.getAllValue()

def main():

    xem = Xem()
    xem.shootPhoto(1200)
    print image

"""
if __name__ == '__main__':
    #main()

"""
    
