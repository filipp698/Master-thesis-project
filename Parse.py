import csv

class Parse:
    slownik2 = {}
    #klucz i wartość
    # slownik = {"-":0,'n1':1,'n3':2,'n5':3,'n8':4,'n14':5,'n20':6,'n28':7,'n40':8,'n41':9,'n47':10,'n77':11,'n78':12,
    #             'b1':13,'b3':14,'b5':15,'b8':16,'b14':17,'b20':18,'b28':19,'b40':20,'b41':21,'b47':22,'b77':23}
    #odczyt danych TL z pliku csv
    def parseTL(self, pathOder, pathZasoby, pathParse):
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
        inne = []

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
                self.slownik2[value].append(numerZasobu[i])
            else:
                slownik[value] = [numerZasobu[i]]
                self.slownik2[value] = [numerZasobu[i]]
        #print(slownik)
        #print(self.slowo)

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
        #print("Ilosc zasobow: ", len(kodZasobu)-1)
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



