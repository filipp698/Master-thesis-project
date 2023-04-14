import csv

class Parse:
    #klucz i wartość
    # slownik = {"-":0,'n1':1,'n3':2,'n5':3,'n8':4,'n14':5,'n20':6,'n28':7,'n40':8,'n41':9,'n47':10,'n77':11,'n78':12,
    #            'b1':13,'b3':14,'b5':15,'b8':16,'b14':17,'b20':18,'b28':19,'b40':20,'b41':21,'b47':22,'b77':23}
    slownik = {"-": 0, 'n1': 9, 'n3': 37, 'n5': 47, 'n8': 54, 'n14': 30, 'n20': 32, 'n28': 34, 'n40': 39, 'n41': 42, 'n47': 46,
               'n77': 50, 'n78': 52, 'b1': 10, 'b3': 19, 'b5': 25, 'b8': 28, 'b14': 13, 'b20': 14, 'b28': 17, 'b40': 22, 'b41': 23, 'b47': 24,
               'b77': 56}
    #odczyt danych TL z pliku csv
    def parse_TL(self):
        path = "Dane\\orders-opis.csv"
        path2 = "Dane\\zasoby.csv"
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


        with open(path2) as Zasoby:
            reader = csv.DictReader(Zasoby, delimiter=";")
            for line in reader:
                numerZasobu.append(line['NR']) #1,2,3
                kodZasobu.append(line['KOD']) #TL1,TL2
                inne.append(line['inne'])
            #print(numerZasobu)
            #print(kodZasobu)
        #print(inne)
        my_dict = {}
        #my_dict = {kodZasobu[i]: numerZasobu[i] for i in range(len(kodZasobu))}
        for i, value in enumerate(kodZasobu):
            if value in my_dict:
                my_dict[value].append(numerZasobu[i])
            else:
                my_dict[value] = [numerZasobu[i]]
        print(my_dict)
        #radiaFDD = ['n1','n3','n5','n8','n14','n20','n28']

        #print(radiaFDD)
        #print(radiaTDD)

        with open(path) as daneTL:
            reader = csv.DictReader(daneTL, delimiter=";")
            for line in reader:
                nrZam.append(line['Numer_zamowienia'])
                band5G.append(line['Badane pasmo 5G'])
                add5G.append(line['Dodatkowe pasmo 5G'])
                band4G.append(line['Badane pasmo 4G'])
                dl_sesji.append(line['Dlugosc trwania sesji'])
                koniec_sesji.append(line['Pozadany tydzien zakonczenia'])
            for i in range(len(nrZam)):
                if band5G[i] or band4G[i] or add5G[i] in my_dict:
                    band5G[i] = my_dict[band5G[i]]
                    band4G[i] = my_dict[band4G[i]]
                    add5G[i] = my_dict[add5G[i]]
                iloscNR.append(bool(band5G[i]) if band5G[i][0] != '0' else 0)
                iloscLTE.append(bool(band4G[i]) if band4G[i][0] != '0' else 0)
                addRU.append(bool(add5G[i]) if add5G[i][0] != '0' else 0)
                suma = iloscNR[i] + iloscLTE[i] + addRU[i] + 1
                iloscRU.append(suma)
        print("Ilosc zasobow: ", len(kodZasobu))
        print("Ilosc zamowien: ",len(nrZam))
        #print("Bandy NR:",band5G)
        #print("Dodatkowe 5G:", add5G)
        #print("Bandy LTE: ", band4G)
        #print("Ilość radii w danym zamówieniu", iloscRU)
        listNR= [] #listy do przechowywania radii przy zapisywaniu danych
        listLTE = []
        listAdd = []
        dict = {'n40': my_dict['n40'], 'n41': my_dict['n41'], 'n47': my_dict['n47'], 'n77': my_dict['n77'],
                'n78': my_dict['n78']}
        dict2 = {'n40': 39, 'n41': 42, 'n47': 46, 'n77': 50, 'n78': 52}
        print(dict)
        bb = dict2.values()
        print(dict2.values())
        TDD = [6, 7, 8]
        FDD = [1, 2, 3, 4, 5]
        radiaTDD = ['n40', 'n41', 'n47', 'n77', 'n78']
        #slownikFDD = {'TL 1': my_dict['TL 1'], 'TL 2': my_dict['TL 2'], 'TL 3': my_dict['TL 3'],'TL 4': my_dict['TL 4'],'TL 5': my_dict['TL 5']}
        #slownikTDD = {'TL 6': my_dict['TL 6'], 'TL 7': my_dict['TL 7'], 'TL 8': my_dict['TL 8']}
        # for i in range(len(TDD)):
        #     if TDD[i] in slownikTDD:
        #         TDD[i] = slownikTDD[TDD[i]]
        # print(slownikTDD)
        # print(slownikFDD)
        #print(my_dict['n1'])
        # zapis do pliku w odpowiednim formacie
        with open("Dane\\dane_moje.txt", 'w', newline='') as file:
            writer = csv.writer(file, delimiter=' ')
            writer.writerow([len(nrZam),len(kodZasobu)-1])
            for i in range(len(nrZam)):
                writer.writerow([nrZam[i],dl_sesji[i],koniec_sesji[i], iloscRU[i]])
                if int(band5G[i][0]) in dict2.values():
                    writer.writerow([len(TDD),TDD])
                else:
                    writer.writerow([len(FDD),FDD])
                for j in range(len(band5G[i])):
                    listNR.append(band5G[i][j])
                    # if band5G[i][j] in dict['n40']:
                    #     writer.writerow([TDD])
                listNR.insert(0,len(band5G[i]))
                writer.writerow(listNR)
                listNR.clear()
                for j in range(len(add5G[i])):
                    #if add5G[i] != my_dict['-']:
                    listAdd.append(add5G[i][j])
                if listAdd != my_dict['-']:
                    listAdd.insert(0, len(add5G[i]))
                    writer.writerow(listAdd)
                listAdd.clear()
                for j in range(len(band4G[i])):
                    #if band4G[i] != my_dict['-']:
                    listLTE.append(band4G[i][j])
                if listLTE != my_dict['-']:
                    listLTE.insert(0, len(band4G[i]))
                    writer.writerow(listLTE)
                listLTE.clear()
                #writer.writerow([len(band5G[i]),band5G[i]])
                #if add5G[i] != my_dict['-']: writer.writerow([len(add5G[i]), add5G[i]])
                #if band4G[i] != my_dict['-']: writer.writerow([len(band4G[i]), band4G[i]])

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
        iloscNR = []
        iloscLTE = []
        add = []
        addRU =[]
        iloscRU = []
        #Otwarcie pliku csv i odczyt danych
        with open(path, encoding='utf-8-sig') as dane_order:
            reader = csv.DictReader(dane_order, delimiter=";")
            for line in reader:
                band5G.append(line['Pasmo5G'])
                band4G.append(line['Pasmo4G'])
                nrZam.append(line['Nrzam'])
                add.append(line['Dodatkowe5G'])
                #iloscRU.append(len(['Pasmo5G']+['Pasmo4G']))
                #print("Zamówienie nr: " + line['Nrzam'] + " Band 5G: " + line['Pasmo5G'] + " Band 4G: " + line['Pasmo4G'])

            #Porównanie wartości bandów z kluczem słownikowym i ich zamiana
            for i in range(len(nrZam)):
                if band5G[i] or band4G[i] or add[i] in self.slownik:
                    band5G[i] = self.slownik[band5G[i]]
                    band4G[i] = self.slownik[band4G[i]]
                    add[i] = self.slownik[add[i]]
                iloscNR.append(bool(band5G[i]) if band5G[i] != 0 else 0)
                iloscLTE.append(bool(band4G[i]) if band4G[i] != 0 else 0)
                addRU.append(bool(add[i]) if add[i] != 0 else 0)
                suma = iloscNR[i] + iloscLTE[i] + addRU[i]
                iloscRU.append(suma)

        #zapis do pliku w odpowiednim formacie
        with open("Dane\\order.txt",'w',newline='') as file:
            writer = csv.writer(file)
            writer.writerow([len(nrZam)])
            for i in range(len(nrZam)):
                writer.writerow([nrZam[i],iloscRU[i],band5G[i],add[i],band4G[i]])

