import numpy as np
#pj - dlugosc sesji, dj - pozadany koniec sesji
def wczytaj_dane(nazwa_pliku):
    tasks = []
    zasobyTL = []
    dataOrder = []
    zas_zad = []
    dl_sesji = []
    koniec_sesji = []
    nr_zam = []
    with open(nazwa_pliku, 'r') as plik:
        ilosc_zadan, ilosc_zasobow = map(int, plik.readline().strip().split())
        for i in range(ilosc_zadan):
            nr, pj, dj, zasoby_zad = map(int, plik.readline().strip().split())
            zasoby = []
            zas_zad.append(zasoby_zad)
            dl_sesji.append(pj)
            koniec_sesji.append(dj)
            nr_zam.append(nr)
            for j in range(zasoby_zad):
                zasoby.append(list(map(int, plik.readline().strip().split())))
            zasobyTL.append(zasoby)
            dataOrder.append([nr,pj,dj])
            tasks.append([nr,pj,dj, zasoby])
    return tasks,ilosc_zadan,ilosc_zasobow,zasobyTL,dataOrder,zas_zad,dl_sesji,koniec_sesji,nr_zam

def wykonaj_algorytm():
    path = 'Dane\\data_prog.txt'
    tasks, iloscZamowien, iloscZasobow, zasobyTL, dataOrder, z, pj, dj, nr_zam = wczytaj_dane(path)

    print("Numery zamówień: ",nr_zam)
    print("Zasoby:", zasobyTL)
    print("Dane zamówienia: ", dataOrder)
    print("Ilosc zasobow wykorzystywanych w kazdym zadaniu: ",z)
    print("Dlugosci trwania poszczególnych sesji: ", pj)
    print("Pożadane końce sesji: ",dj)
    R = []  # moment zwolnienia zasobu
    #j = []  # możliwe permutacje zamówień
    #u = []  # lista urządzeń przyporządkowana do wykonania zadania
    u = [[0 for i in range(z[j])] for j in range(iloscZamowien)]
    S = [] #momenty rozpoczęcia
    C = [] #momenty zakończenia
    Z = [i for i in range(iloscZasobow)]
    for i in range(iloscZasobow):
        R.append(int(0))
    for i in range(iloscZamowien):
        j = nr_zam[i]
    #pierwszy etap
        for t in range(z[j-1]):
            # # wyznaczanie momentu zwolnienia zasobu
            # z = Z[j - 1][t]  # indeks zasobu
            # i = u[j - 1].index(t)  # indeks urządzenia u_{jt} w liście u_{j-1}
            # C_iz = C[j - 1][i]  # moment zakończenia zadania i na maszynie z
            # R[z] = max(R[z], C_iz)
            #
            # # wyznaczanie urządzenia u_{jt}
            # u[j - 1][t] = zasobyTL[j - 1][t].index(min(zasobyTL[j - 1][t], key=lambda z: R[z]))
            #u[j][t] = min(zasobyTL[j][t], key=lambda z: R[z])
            u[j-1][t] = min(zasobyTL[j-1][t])
            #S[j] = 1
            #u[j-1][t] = min(zasobyTL[j-1][t], key=lambda z:R[z+1])
            #print(u[j][t])
    print(u)

            #a=1
    #print("Możliwe permutacje: ",j)
    #print("Zasoby potrzebne do wykonania danego zamówienia: ", min(zasobyTL[0][2]))


wykonaj_algorytm()

