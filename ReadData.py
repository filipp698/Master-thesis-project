class ReadData:
    u = [] #lista urządzeń
    Sj = [] #momenty rozpoczęcia
    Cj = [] #momenty zakończenia
    Tj = [] #spoznienia
    R = []
    suma_kar = 0

    def __init__(self,path):
        _, iloscZamowien, _, _, _, _, _, _, permutation = self.wczytaj_dane(path)
        self.firstPermutation = permutation

    def wczytaj_dane(self,nazwa_pliku):
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

    def wykonaj_algorytm(self, permutacja, path):
        tasks, iloscZamowien, iloscZasobow, zasobyTL, dataOrder, z, p, d, _ = self.wczytaj_dane(path)
        nr_zam = permutacja
        R = []  # moment zwolnienia zasobu
        Sj = []
        Cj = []
        Tj = []
        u = [[0 for i in range(z[j])] for j in range(iloscZamowien)]
        for i in range(iloscZasobow + 1):
            R.append(0)
        for i in range(iloscZamowien):
            j = nr_zam[i]  # możliwe permutacje zamówień
            # pierwszy etap
            for t in range(1, (z[j - 1] + 1)):
                u[j - 1][t - 1] = min(zasobyTL[j - 1][t - 1][1:], key=lambda z: R[z])  # lista list
            # drugi etap
            S = R[u[j - 1][0]]  # moment rozpoczęcia wynosi moment zwolnienia danej TL
            Sj.append(R[u[j - 1][0]])
            for t in range(2, (z[j - 1] + 1)):  # indeksowanie się po radiach
                if S < R[u[j - 1][
                    t - 1]]:  # jeśli mooment rozpoczęcia będzie mniejszy niż dostępne radio to zmieniamy go na wartość dostępności RU
                    S = R[u[j - 1][t - 1]]
            # trzeci etap
            C = S + p[j - 1]  # moment zakończenia
            Cj.append(S + p[j - 1])
            T = C - d[j - 1]
            if T > 0:
                Tj.append(C - d[j - 1])
            elif T <= 0:
                Tj.append(0)
            # czwarty etap
            for t in range(1, (z[j - 1] + 1)):
                R[u[j - 1][t - 1]] = C
        suma_kar = sum(Tj)
        #print("Suma spoznien wynosi: ", suma_kar)
        # with open("Dane\\wyniki.txt", "w") as file:
        #     for i in range(len(Sj)):
        #         file.write(str(Sj[i]) +" ")
        #         file.write(str(Cj[i]) +" : ")
        #         file.write(str(u[i]) + "\n")
        #     file.write('Suma spoznien wynosi: ' + str(suma_kar) + '\n')
        return u,Sj,Cj,suma_kar

    def zapisz_wynik(self,pathData,pathWynik):
        permutacja = self.firstPermutation
        u,Sj,Cj,suma_kar = self.wykonaj_algorytm(permutacja, pathData)
        # print("Lista urządzeń potrzebnych do wykonania zadań:",self.u)
        # print("Momenty rozpoczęcia zadań: ", self.Sj)
        # print("Momenty zakończenia zadań: ", self.Cj)
        # print("Funkcja kary: ", self.Tj)
        #suma_kar = sum(Tj)
        print("Suma spóźnień: ", suma_kar)
        with open(pathWynik,"w") as file:
            for i in range(len(Sj)):
                file.write(str(Sj[i]) +" ")
                file.write(str(Cj[i]) +" : ")
                file.write(str(u[i]) + "\n")
            file.write('Suma spoznien wynosi: ' + str(suma_kar) + '\n')
        return


