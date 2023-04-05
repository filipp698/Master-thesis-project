import csv
import numpy as np

#class SPT:
def importData():
    zmienna = []
    zasoby = []
    TL = []
    # with open('Dane\\data_prog.txt', 'r') as daneTL:
    #     first_line = daneTL.readline()  # odczytaj pierwszy wiersz
    #     third_element = int(first_line.split()[3])  # odczytaj trzeci element (indeks 2) z pierwszego wiersza i zamień na liczbę całkowitą
    #     data = []  # utwórz pustą listę na dane
    #     for i in range(third_element):
    #         line = daneTL.readline().strip()  # odczytaj jedną linię i usuń znaki końca linii
    #         data.append(line.split())  # rozdziel linię na elementy i dodaj je do listy danych
    #     # zrób coś z wczytanymi danymi, np. wyświetl je
    #     print(data)

    # with open('Dane\\data_prog.txt', 'r') as daneTL:
    #     for line in daneTL:
    #         values = line.split()  # rozdziel wartości z wiersza
    #         numbers = [int(x) for x in values]  # zamień wartości na liczby całkowite
    #         #print(numbers)  # wyświetl liczby jako listę

    daneTL = open("Dane\\data_prog.txt")
    zawartosc = daneTL.read()
    wiersze = zawartosc.split("\n")
    liczby = wiersze[1:]
    pierwszyWiersz = wiersze[0].split(" ")
    iloscOrder = int(pierwszyWiersz[0])
    iloscZasobow = int(pierwszyWiersz[1])
    C = np.zeros((iloscOrder,2))
    S = np.zeros((iloscOrder,2))
    for i in range(len(liczby)):
        zmienna.append(liczby[i].split())
        #print(zmienna[i])
    zasoby = int(zmienna[0][3])
    print(zasoby)
    for i in range(zasoby):
        print(zmienna[i+1])
        #zasoby = zmienna[i+2][3]
    print(zasoby)
    #print(zmienna)

#czasy wykonania zapisać w tablicy (numpy np.)
#kary - suma spóźnień
    #print("Ilosc zasobów: ", zmienna[1][3])
    #print("Ilosc zamowien: ", iloscOrder)
    #print("Ilosc zasobow: ", iloscZasobow)
    #print(zmienna)
    #print(wiersze)

    daneTL.close()

importData()
    #     reader = csv.DictReader(daneTL, delimiter=" ")
    #     for line in reader:
    #         bandsNR.append(line['Bandy5G'].split(','))
    #         bandsLTE.append(line['Bandy4G'].split(','))
    #         nrTL.append(line['NrTL'])
    # print(bandsNR)
    # print(bandsLTE)
    # print(nrTL)
