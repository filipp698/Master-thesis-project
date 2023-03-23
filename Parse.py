import csv

class Parse:
    #klucz i wartość
    slownik = {"-":0,'n1':1,'n3':2,'n5':3,'n8':4,'n14':5,'n20':6,'n28':7,'n40':8,'n41':9,'n47':10,'n77':11,'n78':12,
               'b1':13,'b3':14,'b5':15,'b8':16,'b14':17,'b20':18,'b28':19,'b40':20,'b41':21,'b47':22}

    #odczyt danych TL z pliku csv
    def importTL(self,path):
        nrTL = []
        bandsNR = []
        bandsLTE = []
        with open(path, encoding='utf-8-sig') as daneTL:
            reader = csv.DictReader(daneTL, delimiter=";")
            for line in reader:
                bandsNR.append(line['Bandy5G'].split(','))
                bandsLTE.append(line['Bandy4G'].split(','))
                nrTL.append(line['NrTL'])
                #print(line['NrTL'] + " Bandy NR: " + line['Bandy5G']+ " Bandy LTE: " + line['Bandy4G'])
                #print(bandsNR)

        #Parsowanie linii pod radia NR
            for listNR in bandsNR:
                for i in range(len(listNR)):
                    if listNR[i] in self.slownik:
                        listNR[i] = self.slownik[listNR[i]]
        #Parsowanie linii pod radia LTE
            for listLTE in bandsLTE:
                for i in range(len(listLTE)):
                    if listLTE[i] in self.slownik:
                        listLTE[i] = self.slownik[listLTE[i]]
            #print(bandsNR)
            #print(bandsLTE)
    #Wczytywanie danych do formatu txt
        with open("Dane\\testlines.txt",'w',newline='') as file:
            writer = csv.writer(file, delimiter=";")
            for i in range(len(nrTL)):
                iloscRU = len(bandsNR[i] + bandsLTE[i])
                #NR = [str(i) for i in bandsNR]
                #LTE = [str(i) for i in bandsLTE]
                writer.writerow([nrTL[i], iloscRU, bandsNR[i], bandsLTE[i]])

    #wczytywanie danych radii z pliku csv
    def importRU(self,path):
        iloscRU = []
        bandy = []
        with open(path, encoding='utf-8-sig') as daneRUs:
            reader = csv.DictReader(daneRUs, delimiter=";")
            for line in reader:
                bandy.append(line['Band'])
                iloscRU.append(line['IloscRU'])
                #print("Band " + line['Band'] + " Ilosc radii: " + line['IloscRUs'])
        #print(bandy)
        for i in range(len(bandy)):
            if bandy[i] in self.slownik:
                bandy[i] = self.slownik[bandy[i]]
        #zapis do pliku w odpowiednim formacie
        with open("Dane\\radia.txt",'w',newline='') as file:
            writer = csv.writer(file)
            for k in range(len(bandy)):
                writer.writerow([bandy[k],iloscRU[k]])

    #wczytywanie listy zamówień z pliku csv
    def importOrder(self,path):
        band5G = []
        band4G = []
        nrZam = []
        iloscRU = []
        add = []
        #Otwarcie pliku csv i odczyt danych
        with open(path, encoding='utf-8-sig') as dane_order:
            reader = csv.DictReader(dane_order, delimiter=";")
            for line in reader:
                band5G.append(line['Pasmo5G'])
                band4G.append(line['Pasmo4G'])
                nrZam.append(line['Nrzam'])
                add.append(line['Dodatkowe5G'])
                iloscRU.append(len(['Pasmo5G']+['Pasmo4G']))
                #print("Zamówienie nr: " + line['Nrzam'] + " Band 5G: " + line['Pasmo5G'] + " Band 4G: " + line['Pasmo4G'])
            #print(band5G)
            print(band5G[0])
            #Porównanie wartości bandów z kluczem słownikowym i ich zamiana
            for i in range(len(nrZam)):
                if band5G[i] or band4G[i] and add[i] in self.slownik:
                    band5G[i] = self.slownik[band5G[i]]
                    band4G[i] = self.slownik[band4G[i]]
                    add[i] = self.slownik[add[i]]
            #print(band5G)
        #zapis do pliku w odpowiednim formacie
        with open("Dane\\order.txt",'w',newline='') as file:
            writer = csv.writer(file)
            writer.writerow([len(nrZam)])
            for k in range(len(nrZam)):
                writer.writerow([nrZam[k],iloscRU[k],band5G[k],add[k],band4G[k]])

