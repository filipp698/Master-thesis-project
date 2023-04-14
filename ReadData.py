class ReadData:
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

    def wykonaj_algorytm(self,path):
        tasks, iloscZamowien, iloscZasobow, zasobyTL, dataOrder, z, p, d, nr_zam = self.wczytaj_dane(path)
        #print("Numery zamówień: ",nr_zam)
        #print("Zasoby:", zasobyTL)
        #("Dane zamówienia: ", dataOrder)
        print("Ilosc zasobow wykorzystywanych w kazdym zadaniu: ",z)
        print("Dlugosci trwania poszczególnych sesji: ", p)
        print("Pożadane końce sesji: ",d)
        R = []  # moment zwolnienia zasobu
        u = [[0 for i in range(z[j])] for j in range(iloscZamowien)]
        Cj = [] #momenty zakończenia
        Sj = [] #momenty rozpoczęcia
        for i in range(iloscZasobow+1):
            R.append(0)
        for i in range(iloscZamowien):
            j = nr_zam[i] #możliwe permutacje zamówień
        #pierwszy etap
            for t in range(1,(z[j-1]+1)):
                u[j-1][t-1] = min(zasobyTL[j-1][t-1][1:], key=lambda z: R[z]) #lista list
                #ujt2.append(min(zasobyTL[j - 1][t-1][1:], key=lambda z: R[z])) #pojedyncza lista
            #drugi etap
            S = R[u[j-1][0]] #moment rozpoczęcia wynosi moment zwolnienia danej TL
            Sj.append(R[u[j-1][0]])
            for t in range(2,(z[j-1]+1)): #indeksowanie się po radiach
                if S < R[u[j-1][t-1]]: #jeśli mooment rozpoczęcia będzie mniejszy niż dostępne radio to zmieniamy go na wartość dostępności RU
                    S = R[u[j-1][t-1]]
            #trzeci etap
            C = S + p[j-1] #moment zakończenia
            Cj.append(S + p[j-1])
            #czwarty etap
            for t in range(1,(z[j-1]+1)):
                R[u[j-1][t-1]] = C

        print("Lista urządzeń potrzebnych do wykonania zadań:",u)
        print("Momenty rozpoczęcia zadań: ", Sj)
        print("Momenty zakończenia zadań: ", Cj)
        with open("Dane\\wyniki.txt","w") as file:
            for i in range(len(Sj)):
                file.write(str(Sj[i]) +" ")
                file.write(str(Cj[i]) +" : ")
                file.write(str(u[i]) + "\n")
        return u,Sj,Cj


