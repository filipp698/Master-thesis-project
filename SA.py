import random
import time
import math
import csv
import numpy as np
from ReadData import ReadData


class SA(ReadData):
    firstPermutation = np.zeros(3, dtype=int)
    n = 0
    changesOccured = True
    newPermutation = []
    bestDelay = 9999
    bestPermutation = []
    # def __init__(self):
    #     pass

    def createFirstPermutation(self, path):
        _, iloscZamowien, _, _, _, _, _, _, permutation = self.readData(path)
        #self.firstPermutation = self.generateRandomPermutation(permutation)
        self.firstPermutation = permutation
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

    def SA(self, initialPermutation, maxIteration, tmax, tmin, alpha, path):
        start1 = time.time()
        temp = tmax
        currentPermutation = initialPermutation
        _, _, _, _, currentDelay = self.makeSchedule(currentPermutation, path)
        self.bestPermutation = currentPermutation
        _, _, _, _, self.bestDelay = self.makeSchedule(initialPermutation, path)
        self.bestDelay = currentDelay

        while (temp > tmin):
            for k in range(maxIteration):
                start_interation = time.time()
                # szukamy losowo krawędzi do stworzenia rozwiązania
                i = np.random.randint(1, self.n)
                j = np.random.randint(1, self.n)
                # generujemy te rozwiązanie
                newPermutation = self.swap(currentPermutation, i, j)
                # sprawdzamy, czy spełnia warunki przyjęcia
                _, _, _, _, currentBestDelay = self.makeSchedule(currentPermutation, path)
                _, _, _, _, newDelay = self.makeSchedule(newPermutation, path)
                if newDelay < self.bestDelay:
                    self.bestDelay = newDelay
                    self.bestPermutation = newPermutation
                delta = newDelay - currentBestDelay
                probabilityOfAcceptance = random.uniform(0, 1)
                if delta <= 0:
                    currentPermutation = newPermutation
                else:
                    probability = math.exp(-delta / temp)
                    if probability >= probabilityOfAcceptance:
                        currentPermutation = newPermutation
                end_iteration = time.time()
                self.durationOfIteration = end_iteration - start_interation
                # print("Czas trwania iteracji wynosi: ", durationOfIteration)
            temp *= alpha
        end1 = time.time()
        self.durationSA = end1 - start1
        u, Sj, Cj, Tj, suma_spoznien = self.makeSchedule(self.bestPermutation, path)
        print("Suma spoznien: ", suma_spoznien)
        print("Najlepsza premutacja: ", self.bestPermutation)
        # if suma_spoznien !=0:
        #     newPermutation = self.removeTask(self.firstPermutation,path)
        #     _, _, _, _, suma_spoznien = self.makeSchedule(newPermutation, path)
        # return self.firstPermutation
    def SA2(self,permutation, maxIteration, tmax, tmin, alpha, path):
        start1 = time.time()
        temp = tmax
        while (temp > tmin):
            for k in range(maxIteration):
                start_interation = time.time()
                # szukamy losowo krawędzi do stworzenia rozwiązania
                i = np.random.randint(1, self.n)
                j = np.random.randint(1, self.n)
                # generujemy te rozwiązanie
                newPermutation = self.swap(permutation, i, j)
                # sprawdzamy, czy spełnia warunki przyjęcia
                _, _, _, _, currentBestLen = self.makeSchedule(permutation, path)
                _, _, _, _, newLen = self.makeSchedule(newPermutation, path)
                delta = newLen - currentBestLen
                probabilityOfAcceptance = random.uniform(0, 1)
                if delta < 0:
                    permutation = newPermutation
                else:
                    probability = math.exp(-delta / temp)
                    if probability >= probabilityOfAcceptance:
                        permutation = newPermutation
                # if self.Power(self.firstPermutation, newPermutation, temp, path) >= probabilityOfAcceptance:
                #     self.firstPermutation = newPermutation
                end_iteration = time.time()
                self.durationOfIteration = end_iteration - start_interation
                # print("Czas trwania iteracji wynosi: ", durationOfIteration)
            temp *= alpha
        end1 = time.time()
        self.durationSA = end1 - start1
        u, Sj, Cj, Tj, suma_spoznien = self.makeSchedule(permutation, path)
        print("Suma spoznien: ", suma_spoznien)
        return permutation

    def removeTask(self, currentPermutation, path):
        u, Sj, Cj, Tj, suma_spoznien = self.makeSchedule(currentPermutation, path)
        print("Obecnie najlepsza permutacja: ", currentPermutation)
        print("Suma spóźnień: ", suma_spoznien)
        print("Lista spożnien: ", Tj)
        maxDelay = max(Tj)
        print("Usunięta wartość: ", maxDelay)
        index = Tj.index(maxDelay)
        #del u[index]
        #del Sj[index]
        #del Cj[index]
        print("Usunięty index: ", index)
        newPermutation = np.delete(currentPermutation, index)
        print("Permutacja po zmianie: ", newPermutation)
        # filename = "daneAlg\\dane25_4.csv"
        # with open(filename, 'r') as file:
        #     rows = list(csv.reader(file))
        #     del rows[index]
        # with open(filename, 'w',newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerows(rows)
        u1, Sj1, Cj1, Tj1, sumDelay = self.makeSchedule(newPermutation,path)
        print("Suma spoznien: ", sumDelay)
        return newPermutation

        # for i in Tj:
        #     if Tj[i] != 0:
        #         self.firstPermutation[i]
        # self.firstPermutation = self.firstPermutation.remove
    # def result(self,pathWynik):
    #     with open(pathWynik, "w") as file:
    #         for i in range(len(Sj1)):
    #             file.write("Zad " + str(self.newPermutation[i]) + ": ")
    #             file.write(str(Sj1[i]) + " ")
    #             file.write(str(Cj1[i]) + " : ")
    #             file.write(str(u1[i]) + "\n")
    #         file.write('Suma spoznien wynosi: ' + str(sumDelay) + '\n')
    #         file.write('Czas trwania iteracji wynosi: ' + str(self.durationOfIteration) + " [s]" + '\n')
    #         file.write('Czas trwania algorytmu: ' + str(round(self.durationSA, 3)) + " [s]" + '\n')
    #     print(self.tour.astype(int))
    #     print("Suma spóźnień: ", (self.wykonaj_algorytm(self.tour,path)))

    def generateRandomPermutation(self, permutation):
        permutation = np.random.permutation(permutation)
        return permutation


