import csv

#klucz i wartość
slownik = {"-":0,'n1':1,'n3':2,'n5':3,'n8':4,'n14':5,'n20':6,'n28':7,'n40':8,'n41':9,'n47':10,'n77':11,'n78':12,
           'b1':13,'b3':14,'b5':15,'b8':16,'b14':17,'b20':18,'b28':19,'b40':20,'b41':21,'b47':22}
# print(slownik.keys())
# print(slownik.values())

def importTL():
    nrTL = []
    bandsNR = []
    bandsLTE = []
    with open("Dane\\dane_testlines.csv", encoding='utf-8-sig') as daneTL:
        reader = csv.DictReader(daneTL, delimiter=";")
        for line in reader:
            bandsNR.append(line['Bandy5G'].split(','))
            bandsLTE.append(line['Bandy4G'].split(','))
            nrTL.append(line['NrTL'])
            #print(line['NrTL'] + " Bandy NR: " + line['Bandy5G']+ " Bandy LTE: " + line['Bandy4G'])
        print(nrTL)
        #print(bandsNR)
        #print(bandsLTE)
        #print(bandsNR[1])
        #print(len(bandsNR))

        for listNR in bandsNR:
            for i in range(len(listNR)):
                if listNR[i] in slownik:
                    listNR[i] = slownik[listNR[i]]
        # print(bandsNR)
        # print(len(listNR))
        # print(listNR)

        for listLTE in bandsLTE:
            for i in range(len(listLTE)):
                if listLTE[i] in slownik:
                    listLTE[i] = slownik[listLTE[i]]
        print(bandsLTE[0])
        # print(len(listNR))
        # print(len(bandsNR))
        # print(listLTE)

#Poprawić wczytywanie danych
    with open("Dane\\testlines.txt",'w',newline='') as file:
        writer = csv.writer(file)
        for i in range(len(nrTL)):
            iloscRU = len(bandsNR[i] + bandsLTE[i])
            writer.writerow([nrTL[i], iloscRU, bandsNR[i], bandsLTE[i]])

def importRU():
    iloscRU = []
    bandy = []
    with open("Dane\\dane_radia.csv", encoding='utf-8-sig') as daneRUs:
        reader = csv.DictReader(daneRUs, delimiter=";")
        for line in reader:
            iloscRU.append(line['IloscRUs'])
            bandy.append((line['Band']))
            #print("Band " + line['Band'] + " Ilosc radii: " + line['IloscRUs'])
    #print(bandy)
    for i in range(len(bandy)):
        if bandy[i] in slownik:
            bandy[i] = slownik[bandy[i]]
    print(bandy)
        # for j in slownik:
        #     if i == slownik[j]:
        #         bandy[i] = slownik[bandy[i]]
    with open("Dane\\radia.txt",'w',newline='') as file:
        writer = csv.writer(file)
        for k in range(len(bandy)):
            writer.writerow([bandy[k],iloscRU[k]])

def importOrder():
    band5G = []
    band4G = []
    nrZam = []
    iloscRU = []
    #Otwarcie pliku csv i odczyt danych
    with open("Dane\\dane_order.csv", encoding='utf-8-sig') as dane_order:
        reader = csv.DictReader(dane_order, delimiter=";")
        for line in reader:
            band5G.append(line['Pasmo5G'])
            band4G.append(line['Pasmo4G'])
            nrZam.append(line['Nrzam'])
            iloscRU.append(len(['Pasmo5G']+['Pasmo4G']))
            print("Zamówienie nr: " + line['Nrzam'] + " Band 5G: " + line['Pasmo5G'] + " Band 4G: " + line['Pasmo4G'])
        #Porównanie wartości bandów z kluczem słownikowym i ich zamiana
        for i in range(len(nrZam)):
            if band5G[i] or band4G[i] in slownik:
                band5G[i] = slownik[band5G[i]]
                band4G[i] = slownik[band4G[i]]
            # for j in slownik:
            #     if i == slownik[j]:
            #         band5G[i] = slownik[band5G[i]]
            #         band4G[i] = slownik[band4G[i]]

        print("Po zamianie:", band5G)
        print("Po zamianie:", band4G)

    with open("Dane\\order.txt",'w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([len(nrZam)])
        for k in range(len(nrZam)):
            writer.writerow([nrZam[k],iloscRU[k],band5G[k],band4G[k]])

#importOrder()
#importRU()
importTL()
