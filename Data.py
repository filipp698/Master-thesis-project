import string
import numpy as np


class Data:
    bandNR = []
    bandLTE = []
    timeStart = np.zeros(3)
    timeEnd = np.zeros(3)
    ammountNR = np.zeros(3)
    ammountLTE = np.zeros(3)

    def __int__(self):
        pass

    def importRU(self,path):
        f = open(path)
        data = f.read()
        newline = data.split("\n")
        ammount = len(newline)
        ammountNR = np.zeros((ammount),dtype=int)
        ammountLTE = np.zeros((ammount),dtype=int)
        availableBands = []
        for i in range(ammount):
            daneRU = newline[i].split()
            availableBands.append(daneRU[0])
            ammountNR[i] = int(daneRU[1])
            ammountLTE[i] = int(daneRU[2])
        ammountRU = (ammountNR+ammountLTE).sum()
        print("Dostepne pasma częstotliwościowe: ", availableBands)
        print("Dostepne radia 5G: ", ammountNR)
        print("Dostepne radia 4G: ", ammountLTE)
        print("Całkowita ilość radiów w laboratorium: ",ammountRU)
        f.close()
        self.ammountNR = ammountNR
        self.ammountLTE = ammountLTE

    def importTL(self,path):
        f = open(path)
        data = f.read()
        newline = data.split("\n")
        ammount = len(newline)
        print("Dostepne testlinie:")
        for i in range(ammount):
            daneTL = newline[i].split()
            print(daneTL)

    def importOrder(self,path):
        f = open(path)
        data = f.read()
        newline = data.split("\n")
        TL = int(newline[0])
        daneTL = []
        bandNR = []
        bandLTE = []
        timeStart = np.zeros((TL),dtype=int)
        timeEnd = np.zeros((TL),dtype=int)
        typeSession = []

        for i in range(TL):
            daneTL = newline[i+1].split()
            typeSession.append(daneTL[2])
            bandNR.append(daneTL[3])
            bandLTE.append(daneTL[4])
            #bandNR[i] = int(daneTL[3])
            #bandLTE[i] = int(daneTL[4])
            timeStart[i] = int(daneTL[5])
            timeEnd[i] = int(daneTL[6])
            #print("Szczegóły zamówienia nr:", daneTL)
        print("Bandy NR: ", bandNR)
        print("Bandy LTE: ",bandLTE)
        print("Typ sesji: ", typeSession)
        print("Czasy startów sesji: ", timeStart)
        print("Czasy zakończenia sesji: ", timeEnd)
        f.close()
        self.bandNR = bandNR
        self.bandLTE = bandLTE
        self.timeStart = timeStart
        self.timeEnd = timeEnd
