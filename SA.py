import random
import time

import numpy as np
import matplotlib.pyplot as plt
from ReadData import ReadData


class SA(ReadData):
    firstPermutation = np.zeros(3, dtype=int)
    n = 0
    changesOccured = True
    # def __init__(self):
    #     pass

    def createFirstPermutation(self, path):
        _, iloscZamowien, _, _, _, _, _, _, permutation = self.readData(path)
        self.firstPermutation = self.generateRandomPermutation(permutation)
        #self.firstPermutation = permutation
        self.n = iloscZamowien

    def swap(self, currentTour, i, j):
        newTour = np.copy(currentTour)
        if i <= j:
            partToFlip = np.copy(newTour[i:j + 1])
            newTour[i:j + 1] = np.flip(partToFlip)
        else:
            partToFlip = np.copy(newTour[j:i + 1])
            newTour[j:i + 1] = np.flip(partToFlip)
        return newTour

    def Power(self, currentBestPermutation, newPermutation, temperature, path):
        # obliczenie długości obu tras
        _,_,_,currentBestLen = self.makeSchedule(currentBestPermutation, path)
        _,_,_,newLen = self.makeSchedule(newPermutation, path)
        # jesli wylosowane rozwiązanie jest lepsze od aktualnego,
        # zaktualizuj aktualne
        if newLen <= currentBestLen:
            # zawsze będzie większe od zakresu [0, 1] -> akcpetujemy wynik jako lepszy
            return 2

        # obliczenie różnicy spoznien pomiędzy permutacjami
        #difference = currentBestLen - newLen
        difference = np.abs(currentBestLen - newLen)
        # obliczenie prawdopodobieństwa dla akceptacji
        # wraz ze wzrostem różnicy odległości ono maleje,
        # jednakowo dla temperatury - im mniejsza tym mniejsze prawd.
        propabilityOfAcceptance = 1 / difference * temperature
        # print(propabilityOfAcceptance)

        return propabilityOfAcceptance

    def SA(self, maxIteration, kmax, path, pathWynik):
        start1 = time.time()
        for k in range(maxIteration):
            start_interation = time.time()
            # obliczamy aktualną temperaturę
            if k <= kmax:
                temp = 1 - (k + 1) / kmax
            else:
                temp = 1 / kmax

            # szukamy losowo krawędzi do stworzenia rozwiązania
            i = np.random.randint(1, self.n)
            j = np.random.randint(1, self.n)

            # generujemy te rozwiązanie
            newTour = self.swap(self.firstPermutation, i, j)

            # sprawdzamy, czy spełnia warunki przyjęcia
            #randomProbability = np.random.rand()
            random_value = random.uniform(0.8,0.99)
            probabilityOfAcceptance = random_value * temp

            if self.Power(self.firstPermutation, newTour, temp, path) >= probabilityOfAcceptance:
                self.firstPermutation = newTour
            end_iteration = time.time()
            durationOfIteration = end_iteration - start_interation
            #print("Czas trwania iteracji wynosi: ", durationOfIteration)

        end1 = time.time()
        durationSA = end1 - start1

        u,Sj,Cj,suma_spoznien = self.makeSchedule(self.firstPermutation, path)
        print("Suma spóźnień: ", suma_spoznien)
        with open(pathWynik,"w") as file:
            for i in range(len(Sj)):
                file.write(str(Sj[i]) +" ")
                file.write(str(Cj[i]) +" : ")
                file.write(str(u[i]) + "\n")
            file.write('Suma spoznien wynosi: ' + str(suma_spoznien) + '\n')
            file.write('Czas trwania iteracji wynosi: ' + str(durationOfIteration) + " [s]" + '\n')
            file.write('Czas trwania algorytmu: ' + str(round(durationSA, 3)) + " [s]" + '\n')
        # print(self.tour.astype(int))
        #print("Suma spóźnień: ", (self.wykonaj_algorytm(self.tour,path)))

    def generateRandomPermutation(self, permutation):
        permutation = np.random.permutation(permutation)
        return permutation


