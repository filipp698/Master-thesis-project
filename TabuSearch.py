import numpy as np
import sys
import Queue_
from ReadData import ReadData


class TabuSearch(ReadData):
    firstPermutation = np.zeros(3)
    bestDistance = 9999
    bestPermutation = np.zeros(3)
    bestPermutationHistory = []
    localBestpermutationHistory = []
    permutationHistoryGlobal = []
    permutationHistoryLocal = []
    suma_kar = 0

    def __init__(self,path):
        _, _, _, _, _, _, _, _, permutation = self.wczytaj_dane(path)
        #self.firstPermutation = self.generateRandomPermutation(permutation)
        self.firstPermutation = permutation

    def execute(self, startPermutation, lenghtOfTabu, option, iterationNumber, cycleNumberMax, isReactiveTabu, reactiveInterval,path,pathWynik):
        _,_,_,Tj = self.wykonaj_algorytm(self.firstPermutation,path)
        isCycleNumberMaxReached = False
        intervalIterator = 0
        permutation = startPermutation
        localBestPermutation = startPermutation
        tabuList = Queue_.Queue(lenghtOfTabu)
        tabuList.put(localBestPermutation)
        self.suma_kar = Tj
        ## KONIEC ALGORYTMU

        for xx in range(iterationNumber):
            localBestDistance = sys.maxsize
            neighborhood = self.generateNeighborhood(permutation, option)
            for neighborPermutation in neighborhood:
                isInTabu, index = tabuList.contains(neighborPermutation)
                _,_,_,distance = self.wykonaj_algorytm(neighborPermutation,path) #kalkuluować sumę spóźnień dla danej permutacji
                if distance < localBestDistance:
                    if isInTabu:
                        if self.bestDistance > distance:
                            localBestDistance = distance
                            localBestPermutation = neighborPermutation
                        else:
                            pass
                            # neighborhood.remove(index)
                    else:
                        localBestDistance = distance
                        localBestPermutation = neighborPermutation
            bestPermutationChanged = False
            print(str(xx) + ": " + str(localBestDistance))
            if localBestDistance < self.bestDistance:
                self.bestDistance = localBestDistance
                self.bestPermutation = localBestPermutation
                bestPermutationChanged = True
            permutation = localBestPermutation
            tabuList.put(permutation)
            if bestPermutationChanged:
                cycleNumber = 0
                isCycleNumberMaxReached = False
                intervalIterator = 0
                print("Best permutation found: " + str(self.bestPermutation) + " Suma:" + str(self.bestDistance))
            else:
                if not intervalIterator < reactiveInterval or not isCycleNumberMaxReached:
                    cycleNumber += 1
                else:
                    intervalIterator += 1

                if cycleNumber > cycleNumberMax:
                    if isReactiveTabu:
                        permutation = self.generateRandomPermutation(permutation)
                        cycleNumber = 0
                        isCycleNumberMaxReached = True
                        intervalIterator = 0
                    else:
                        return self.bestPermutation
            self.bestPermutationHistory.append(self.bestDistance)
            self.localBestpermutationHistory.append(localBestDistance)
            self.permutationHistoryGlobal.append(self.bestPermutation)
            self.permutationHistoryLocal.append(localBestPermutation)

            u, Sj, Cj, suma_spoznien = self.wykonaj_algorytm(self.bestPermutation, path)
            with open(pathWynik + option + ".txt", "w") as file:
                for i in range(len(Sj)):
                    file.write(str(Sj[i]) + " ")
                    file.write(str(Cj[i]) + " : ")
                    file.write(str(u[i]) + "\n")
                file.write('Suma spoznien wynosi: ' + str(suma_spoznien) + '\n')

        return self.bestPermutation

    # def oblicz_spoznienia(self,permutacja,path):
    #     tasks, iloscZamowien, iloscZasobow, zasobyTL, dataOrder, z, p, d,_ = self.wczytaj_dane(path)
    #     nr_zam = permutacja
    #     R = []  # moment zwolnienia zasobu
    #     Sj = []
    #     Cj = []
    #     Tj = []
    #     u = [[0 for i in range(z[j])] for j in range(iloscZamowien)]
    #     for i in range(iloscZasobow+1):
    #         R.append(0)
    #     for i in range(iloscZamowien):
    #         j = nr_zam[i] #możliwe permutacje zamówień
    #     #pierwszy etap
    #         for t in range(1,(z[j-1]+1)):
    #             u[j-1][t-1] = min(zasobyTL[j-1][t-1][1:], key=lambda z: R[z]) #lista list
    #         #drugi etap
    #         S = R[u[j-1][0]] #moment rozpoczęcia wynosi moment zwolnienia danej TL
    #         Sj.append(R[u[j-1][0]])
    #         for t in range(2,(z[j-1]+1)): #indeksowanie się po radiach
    #             if S < R[u[j-1][t-1]]: #jeśli mooment rozpoczęcia będzie mniejszy niż dostępne radio to zmieniamy go na wartość dostępności RU
    #                 S = R[u[j-1][t-1]]
    #         #trzeci etap
    #         C = S + p[j-1] #moment zakończenia
    #         Cj.append(S + p[j-1])
    #         T = C - d[j-1]
    #         if T > 0:
    #             Tj.append(C - d[j-1])
    #         elif T <= 0:
    #             Tj.append(0)
    #         #czwarty etap
    #         for t in range(1,(z[j-1]+1)):
    #             R[u[j-1][t-1]] = C
    #     suma_kar = sum(Tj)
    #     with open("Dane\\wynikiSA.txt","w") as file:
    #         for i in range(len(Sj)):
    #             file.write(str(Sj[i]) +" ")
    #             file.write(str(Cj[i]) +" : ")
    #             file.write(str(u[i]) + "\n")
    #         file.write('Suma spoznien wynosi: ' + str(suma_kar) + '\n')
    #     return suma_kar

    def generateNeighborhood(self, permutation, option):
        dictionary = {
            1: "insert",
            2: "swap",
            3: "flip"
        }
        option = option.lower()
        if option == dictionary[1]:
            neighborhood = self.generateNeighborhoodByInsert(permutation)
        if option == dictionary[2]:
            neighborhood = self.generateNeighborhoodBySwap(permutation)
        if option == dictionary[3]:
            neighborhood = self.generateNeighborhoodByFlip(permutation)
        return neighborhood

    def generateNeighborhoodByInsert(self, permutation):
        neighborhood = []
        for i in range(1, len(permutation) - 1):
            for j in range(1, len(permutation) - 1):
                if i != j:
                    value = permutation[i]
                    currentPermutation = np.delete(permutation, i)
                    currentPermutation = np.insert(currentPermutation, j, value)
                    ifFound = False
                    for vector in neighborhood:
                        if np.array_equal(vector, currentPermutation):
                            ifFound = True
                    if not ifFound:
                        neighborhood.append(currentPermutation)
        return neighborhood
    
    def generateNeighborhoodBySwap(self, permutation):
        neighborhood = []
        currentPermutation = np.copy(permutation)
        for i in range(1, len(permutation) - 1):
            for j in range(1, len(permutation) - 1):
                if i != j:
                    currentPermutation = np.copy(permutation)
                    value = currentPermutation[i]
                    currentPermutation[i] = currentPermutation[j]
                    currentPermutation[j] = value
                    ifFound = False
                    for vector in neighborhood:
                        if np.array_equal(vector, currentPermutation):
                            ifFound = True
                    if not ifFound:
                        neighborhood.append(currentPermutation)
        return neighborhood
    
    def generateNeighborhoodByFlip(self, permutation):
        neighborhood = []
        currentPermutation = np.copy(permutation)
        for i in range(1, len(permutation) - 1):
            for j in range(1, len(permutation) - 1):
                if i != j:
                    currentPermutation = np.copy(permutation)
                    part = currentPermutation[i:j+1]
                    currentPermutation[i:j+1] = np.flip(part)
                    ifFound = False
                    for vector in neighborhood:
                        if np.array_equal(vector, currentPermutation):
                            ifFound = True
                    if not ifFound:
                        neighborhood.append(currentPermutation)
        return neighborhood

    def generateRandomPermutation(self, permutation):
        permutation[1 : -1] = np.random.permutation(permutation[1:-1])
        return permutation
