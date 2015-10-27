try :
    import ok
except:
    print "Nun se fa niente"

import datetime


class SensDecoder:

    def __init__(self):

        # Creiamo l'oggetto XEM
        self.xem = ok.FrontPanel()
        # Lista dei valori di pixel della foto
        self.photo = []
        # Numero di pixel da recuperare
        self.pixels = 73 
        self.trigIn = (
            0x40,   # Indirizzo del trigger
            0x00    # Indirizzo del bit da attivare
        )
        # Indirizzo della pipeOut sulla scheda
        self.pipeOut = 0xA0

        # Apriamo la connessione alla scheda
        if (self.xem.OpenBySerial("") != self.xem.NoError):
            print "ATTENZIONE! Errore nell'aprire la FPGA"

        # Inserisco il file .bit nella scheda
        self.xem.ConfigureFPGA('../sensore.bit')

        if self.xem.IsOpen():
            print "Connessione effettuata con la FPGA"
        else:
            print "ATTENZIONE! Errore nell'inserire file .bit!"
            exit

    def scattaFoto(self, raffica=False):

        if raffica:
            # TODO: implementare firmware + software
            # possibilita' di foto a raffica
            pass

        # Attiviamo il trigger che da impulso alla scheda
        self.xem.ActivateTriggerIn(self.trigIn[0], self.trigIn[1])

        self.photo = self.getFifoElem()
        print "Foto scattata correttamente!"

        # Togliamo il primo pixel che e' un glitch del sensore (forse)
        return self.photo[1:]

    def getFifoElem(self):

        """
        Funzione che ritorna una lista contenente i valori numerici
        contenuti nella FIFO sulla FPGA
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

        
