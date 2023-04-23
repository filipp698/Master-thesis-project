import csv

class Parse:
    #klucz i wartość
    # slownik = {"-":0,'n1':1,'n3':2,'n5':3,'n8':4,'n14':5,'n20':6,'n28':7,'n40':8,'n41':9,'n47':10,'n77':11,'n78':12,
    #             'b1':13,'b3':14,'b5':15,'b8':16,'b14':17,'b20':18,'b28':19,'b40':20,'b41':21,'b47':22,'b77':23}
    #odczyt danych TL z pliku csv
    def parse_TL(self,pathOder,pathZasoby,pathParse):
        nrZam = []
        band5G = []
        add5G = []
        band4G = []
        dl_sesji = []
        koniec_sesji = []
        iloscNR = []
        iloscLTE = []
        addRU = []
        iloscRU = []
        numerZasobu = []
        kodZasobu = []
        inne =[]
        #odczyt danych z zasobami
        with open(pathZasoby) as zasoby:
            reader = csv.DictReader(zasoby, delimiter=";")
            for line in reader:
                numerZasobu.append(line['NR']) #1,2,3
                kodZasobu.append(line['KOD']) #TL1,TL2
                inne.append(line['inne'])
        slownik = {}
        for i, value in enumerate(kodZasobu):
            if value in slownik:
                slownik[value].append(numerZasobu[i])
            else:
                slownik[value] = [numerZasobu[i]]
        #print(slownik)

        #odczyt danych zamówień
        with open(pathOder) as daneOrder:
            reader = csv.DictReader(daneOrder, delimiter=";")
            for line in reader:
                nrZam.append(line['Numer zamówienia'])
                band5G.append(line['Badane pasmo 5G'])
                add5G.append(line['Dodatkowe pasmo 5G'])
                band4G.append(line['Badane pasmo 4G'])
                dl_sesji.append(line['Długość trwania sesji (badania poszczególnych  funkcji) [tyg]'])
                koniec_sesji.append(line['Pożądany tydzień zakończenia sesji [tyg]'])
            #zamiana poszczególnych bandów na wartości liczbowe ze słownika
            for i in range(len(nrZam)):
                if band5G[i] or band4G[i] or add5G[i] in slownik:
                    band5G[i] = slownik[band5G[i]]
                    band4G[i] = slownik[band4G[i]]
                    add5G[i] = slownik[add5G[i]]
                #sprawdzenie ilości radii w każdym zamówieniu
                iloscNR.append(bool(band5G[i]) if band5G[i][0] != '0' else 0)
                iloscLTE.append(bool(band4G[i]) if band4G[i][0] != '0' else 0)
                addRU.append(bool(add5G[i]) if add5G[i][0] != '0' else 0)
                suma = iloscNR[i] + iloscLTE[i] + addRU[i] + 1
                iloscRU.append(suma)
        print("Ilosc zasobow: ", len(kodZasobu)-1)
        print("Ilosc zamowien: ",len(nrZam))
        #slownik zawierający bandy TDD, które definiują TL6-8
        dictionaryTDD = {'n40': slownik['n40'], 'n41': slownik['n41'], 'n47': slownik['n47'], 'n77': slownik['n77'],
                'n78': slownik['n78']}
        wartosciTDD = dictionaryTDD.values()
        lista_wartosciTDD = []
        #wylistowanie wartości słownikaTDD, aby znalazły się w jednej liście
        for i in wartosciTDD:
            lista_wartosciTDD.extend(i)
        FDD = [] #listy przechowujące numery zasobów poszczególnych TL
        TDD = []
        #przyporządkowanie poszczególnym TL wartości liczbowych
        for key, value in slownik.items():
            # sprawdzenie, czy klucz zawiera się w pierwszym przedziale
            if key in ['TL 1', 'TL 2', 'TL 3', 'TL 4', 'TL 5']:
                FDD.extend(value)  # dodanie wartości do listy FDD
            # sprawdzenie, czy klucz zawiera się w drugim przedziale
            elif key in ['TL 6', 'TL 7', 'TL 8']:
                TDD.extend(value)

        FDDlista = [] #listy ulatawiajce zapis testlini FDD oraz TDD
        TDDlista = []
        listNR = [] #listy do przechowywania każego rodzaju radii przy zapisywaniu danych
        listLTE = []
        listAdd = []
        # zapis do pliku w odpowiednim formacie
        with open(pathParse, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=' ')
            writer.writerow([len(nrZam),len(kodZasobu)-1]) #pierwsza linijka pliku wyjsciowego
            for i in range(len(nrZam)):
                writer.writerow([nrZam[i],dl_sesji[i],koniec_sesji[i], iloscRU[i]]) #informacje o zamowieniu
                # pierwszy zasób - TL
                if band5G[i][0] in lista_wartosciTDD: #sprawdzenie czy band 5G zawiera się w liście bandów TDD
                    for k in range(len(TDD)):
                        TDDlista.append(TDD[k])
                    TDDlista.insert(0, len(TDD))
                    writer.writerow(TDDlista)
                    TDDlista.clear()
                else: #jeśli nie - band FDD
                    for k in range(len(FDD)):
                        FDDlista.append(FDD[k])
                    FDDlista.insert(0, len(FDD))
                    writer.writerow(FDDlista)
                    FDDlista.clear()
                # drugi zasób - radia 5G
                for j in range(len(band5G[i])):
                    listNR.append(band5G[i][j])
                listNR.insert(0,len(band5G[i]))
                writer.writerow(listNR)
                listNR.clear()
                # trzeci zasób - możliwe dodatkowe radio 5G
                for j in range(len(add5G[i])):
                    listAdd.append(add5G[i][j])
                if listAdd != slownik['-']:
                    listAdd.insert(0, len(add5G[i]))
                    writer.writerow(listAdd)
                listAdd.clear()
                # czwarty zasób - radio 4G
                for j in range(len(band4G[i])):
                    listLTE.append(band4G[i][j])
                if listLTE != slownik['-']:
                    listLTE.insert(0, len(band4G[i]))
                    writer.writerow(listLTE)
                listLTE.clear()

    ##STARY KOD
    # def importTL(self,path):
    #     nrTL = []
    #     bandsNR = []
    #     bandsLTE = []
    #     with open(path, encoding='utf-8-sig') as daneTL:
    #         reader = csv.DictReader(daneTL, delimiter=";")
    #         for line in reader:
    #             bandsNR.append(line['Bandy5G'].split(','))
    #             bandsLTE.append(line['Bandy4G'].split(','))
    #             nrTL.append(line['NrTL'])
    #             #print(line['NrTL'] + " Bandy NR: " + line['Bandy5G']+ " Bandy LTE: " + line['Bandy4G'])
    #     #Parsowanie linii pod radia NR
    #         for listNR in bandsNR:
    #             for i in range(len(listNR)):
    #                 if listNR[i] in self.slownik:
    #                     listNR[i] = self.slownik[listNR[i]]
    #     #Parsowanie linii pod radia LTE
    #         for listLTE in bandsLTE:
    #             for i in range(len(listLTE)):
    #                 if listLTE[i] in self.slownik:
    #                     listLTE[i] = self.slownik[listLTE[i]]
    # #Wczytywanie danych do formatu txt
    #     with open("Dane\\testlines.txt",'w',newline='') as file:
    #         writer = csv.writer(file, delimiter=";")
    #         for i in range(len(nrTL)):
    #             iloscRU = len(bandsNR[i] + bandsLTE[i])
    #             #NR = [str(i) for i in bandsNR]
    #             #LTE = [str(i) for i in bandsLTE]
    #             writer.writerow([nrTL[i], iloscRU, bandsNR[i], bandsLTE[i]])
    #
    # #wczytywanie danych radii z pliku csv
    # def importRU(self,path):
    #     iloscRU = []
    #     bandy = []
    #     with open(path, encoding='utf-8-sig') as daneRUs:
    #         reader = csv.DictReader(daneRUs, delimiter=";")
    #         for line in reader:
    #             bandy.append(line['Band'])
    #             iloscRU.append(line['IloscRU'])
    #             #print("Band " + line['Band'] + " Ilosc radii: " + line['IloscRUs'])
    #     #print(bandy)
    #     for i in range(len(bandy)):
    #         if bandy[i] in self.slownik:
    #             bandy[i] = self.slownik[bandy[i]]
    #     #zapis do pliku w odpowiednim formacie
    #     with open("Dane\\radia.txt",'w',newline='') as file:
    #         writer = csv.writer(file)
    #         for k in range(len(bandy)):
    #             writer.writerow([bandy[k],iloscRU[k]])
    #
    # #wczytywanie listy zamówień z pliku csv
    # def importOrder(self,path):
    #     band5G = []
    #     band4G = []
    #     nrZam = []
    #     iloscNR = []
    #     iloscLTE = []
    #     add = []
    #     addRU =[]
    #     iloscRU = []
    #     #Otwarcie pliku csv i odczyt danych
    #     with open(path, encoding='utf-8-sig') as dane_order:
    #         reader = csv.DictReader(dane_order, delimiter=";")
    #         for line in reader:
    #             band5G.append(line['Pasmo5G'])
    #             band4G.append(line['Pasmo4G'])
    #             nrZam.append(line['Nrzam'])
    #             add.append(line['Dodatkowe5G'])
    #             #iloscRU.append(len(['Pasmo5G']+['Pasmo4G']))
    #             #print("Zamówienie nr: " + line['Nrzam'] + " Band 5G: " + line['Pasmo5G'] + " Band 4G: " + line['Pasmo4G'])
    #
    #         #Porównanie wartości bandów z kluczem słownikowym i ich zamiana
    #         for i in range(len(nrZam)):
    #             if band5G[i] or band4G[i] or add[i] in self.slownik:
    #                 band5G[i] = self.slownik[band5G[i]]
    #                 band4G[i] = self.slownik[band4G[i]]
    #                 add[i] = self.slownik[add[i]]
    #             iloscNR.append(bool(band5G[i]) if band5G[i] != 0 else 0)
    #             iloscLTE.append(bool(band4G[i]) if band4G[i] != 0 else 0)
    #             addRU.append(bool(add[i]) if add[i] != 0 else 0)
    #             suma = iloscNR[i] + iloscLTE[i] + addRU[i]
    #             iloscRU.append(suma)
    #
    #     #zapis do pliku w odpowiednim formacie
    #     with open("Dane\\order.txt",'w',newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow([len(nrZam)])
    #         for i in range(len(nrZam)):
    #             writer.writerow([nrZam[i],iloscRU[i],band5G[i],add[i],band4G[i]])

