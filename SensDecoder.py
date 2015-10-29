try :
    import ok
except:
    print "Nun se fa niente"

import datetime


class SensDecoder:

    trigIn = (
        0x40,   # Port
        0x00,   # Start photo
        0x01,   # Set the counter from WireIns
        0x02    # Restore the downAck
     )
    # Indirizzo della pipeOut sulla scheda
    pipeOut = [
        0xA0,   # Port - Fifo A
        0xA1    # Port - Fifo B
    ]

    wireIn = [
        0x03    # Port
    ]

    wireOut = [
        0x20,   # Port - downAck
        0x21    # Port - fifoCount
    ]
    
    def __init__(self):

        # Creiamo l'oggetto XEM
        self.xem = ok.FrontPanel()
        # Lista dei valori di pixel della foto
        self.photo = []
        # Numero di pixel da recuperare
        self.pixels = 73
        self.count = 0

        # Apriamo la connessione alla scheda
        if (self.xem.OpenBySerial("") != self.xem.NoError):
            print "ATTENZIONE! Errore nell'aprire la FPGA"

        # Inserisco il file .bit nella scheda
        self.xem.ConfigureFPGA('../../sensore.bit')

        if self.xem.IsOpen():
            print "Connessione effettuata con la FPGA"
        else:
            print "ATTENZIONE! Errore nell'inserire file .bit!"
            exit
            
    def setCounter(self, period):

        """
        Set the period of the trigger for taking a photo
        period is in milliseconds
        """
        if (period <= 1200) and (period >= 1):
            self.xem.SetWireInValue(self.wireIn[0], period)
            self.xem.UpdateWireIns()
            self.xem.ActivateTriggerIn(self.trigIn[0], self.trigIn[2])
            return True
        return False

    def scattaFoto(self):

        # Attiviamo il trigger che da impulso alla scheda
        self.xem.ActivateTriggerIn(self.trigIn[0], self.trigIn[1])

    def getFifoCount(self):

        self.xem.UpdateWireOuts()
        self.count = self.xem.GetWireOutValue(self.wireOut[1])
        return self.count
    
    def getAllValue(self):

        if self.count > 0:

            # Delete current photo list
            self.photo = []
            
            wordA = '00' * self.count
            wordB = '00' * self.count

            self.xem.ReadFromPipeOut(self.pipeOut[0], wordA)
            self.xem.ReadFromPipeOut(self.pipeOut[1], wordB)

            for row in range(1,self.count):

                newValue = ''.join((format(ord(wordA[2*row+1]), '08b'),
                                   format(ord(wordA[2*row]), '08b'), 
                                   format(ord(wordB[2*row+1]), '08b'),
                                   format(ord(wordB[2*row]), '08b')))
                self.photo.append(int(newValue,2))
                
            self.count = 0
            return self.photo
        


    def getImage(self):
        
        self.photo = self.getFifoElem()
        print "Foto scattata correttamente!"

        # Togliamo il primo pixel che e' un glitch del sensore (forse)
        return self.photo[1:]

    def getFifoElem(self):

        """
        Funzione che ritorna una lista contenente i valori numerici
        contenuti nella FIFO sulla FPGA

        NO MORE USED
        """

        rawBitString = '00' * self.pixels

        # Get fifo stream
        self.xem.ReadFromPipeOut(self.pipeOut, rawBitString)

        # Trasforma in bytearray
        rawBitString = bytearray(rawBitString)
        # Reverse perche' i dati sono scritti in LittleEndian
        # Prima i bit meno significativi e poi quelli piu' significativi
        rawBitString.reverse()

        # Trasformiamo in binario
        binaryString = ''.join(format(x, '08b') for x in rawBitString)

        numbers = []

        for i in range(self.pixels):
            # Prendiamo tutti i sotto blocchi di dimensione 16
            numbers.append(int((1.0/int(binaryString[i*16:(i+1)*16], 2))*10000))

        # Reverse per rimettere al primo posto i primi
        numbers.reverse()

        return numbers

    def stampaFoto(self):
        # Stampo ogni riga 0 --> 73
        for riga in range(self.pixels):
            stringa = ""
            for img in self.photos:
                 stringa += "%d \t " % (int(img[riga], 2))
            print "%s\n" % stringa


        
