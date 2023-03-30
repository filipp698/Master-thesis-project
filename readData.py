
#pj - dlugosc sesji, dj - pozadany koniec sesji
def wczytaj_dane(nazwa_pliku):
    tasks = []
    zasobyTL = []
    dataOrder = []
    with open(nazwa_pliku, 'r') as plik:
        ilosc_zadan, ilosc_zasobow = map(int, plik.readline().strip().split())
        for i in range(ilosc_zadan):
            nr, pj, dj, zasoby_zad = map(int, plik.readline().strip().split())
            zasoby = []
            for j in range(zasoby_zad):
                zasoby.append(list(map(int, plik.readline().strip().split())))
            zasobyTL.append(zasoby)
            dataOrder.append([nr,pj,dj])
            tasks.append([nr,pj,dj, zasoby])
    return tasks,ilosc_zadan,ilosc_zasobow,zasobyTL,dataOrder

def wykonaj_algorytm():
    path = 'Dane\\data_prog.txt'
    tasks, iloscZamowien, iloscZasobow, zasobyTL, dataOrder = wczytaj_dane(path)
    R = [] #moment zwolnienia zasobu
    j = [] # dane zamówienie
    for i in range(iloscZasobow):
        R.append(int(0))
    for i in range(iloscZamowien):
        tasks[i] = j
    print(R)
    print(j)

wykonaj_algorytm()

