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
    delaySA = 9999
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
        bestPremutation = self.bestPermutation
        ammountOfIteration = 0
        print("Suma spoznien na początku: ", suma_spoznien)
        print("Najlepsza permutacja: ", self.bestPermutation)
        print("Lista spoznionych zadań", Tj)
        ## Wyrzucanie każdego z zadań pojedynczo
        # while self.delaySA != 0:
        #     permutationSA = self.findLongestTasks(bestPremutation, path)
        #     SA2 = self.secondSA(permutationSA, maxIteration, tmax, tmin, alpha, path)
        #     bestPremutation = SA2
        #     ammountOfIteration += 1
        #     if self.delaySA == 0:
        #         print("Spoznienie rowne jest 0")
        # print("Permutacja ostateczna: ", SA2)
        # print("Dlugosc ostatecznej premutacji: ", len(SA2))
        # print("Ilosc iteracji petli while: ", ammountOfIteration)
        ## Wyrzucenie zadań przeterminowanych
        while self.delaySA != 0:
            permutationSA = self.findLongestDelayedTask(bestPremutation, path)
            SA2 = self.secondSA(permutationSA, maxIteration, tmax, tmin, alpha, path)
            bestPremutation = SA2
            ammountOfIteration += 1
            if self.delaySA == 0:
                print("Spoznienie rowne jest 0")
        print("Permutacja ostateczna: ", SA2)
        print("Dlugosc ostatecznej premutacji: ", len(SA2))
        print("Ilosc iteracji petli while: ", ammountOfIteration)

        return self.bestPermutation
    def findLongestTasks(self, permutation, path):
        lista_spoznien = []
        for i in range(0,len(permutation)):
            _, _, _, _, spoznienia = self.makeSchedule2(permutation, i, path)
            lista_spoznien.append(spoznienia)
        minDelay = min(lista_spoznien)  # wartość spoźnienia, które daje najwieksze efekty
        index = lista_spoznien.index(minDelay)
        removedElement = permutation[index]
        newPermutation = np.delete(permutation, index)
        _, _, _, _, delay = self.makeSchedule(newPermutation, path)
        print("Lista spoznien dla danych zadan: ", lista_spoznien)
        print("Index wyrzuconej wartości: ", index)
        print("Usuniete zadanie z permutacji: ", removedElement)
        print("Nowa permutacja: ", newPermutation)
        print("Spoznienie w nowej permutacji: ", delay)
        return newPermutation
    def findLongestDelayedTask(self, permutation, path):
        _,_,_,lista_spoznien,delay = self.makeSchedule(permutation,path)
        delayedTask = 0
        for task in lista_spoznien:
            if task != 0:
                delayedTask = task
                break
        #print(delayedTask)
        index = lista_spoznien.index(delayedTask)
        removedElement = permutation[index]
        newPermutation = np.delete(permutation, index)
        _, _, _, _, delay = self.makeSchedule(newPermutation, path)
        print("Lista spoznien dla danych zadan: ", lista_spoznien)
        print("Index wyrzuconej wartości: ", index)
        print("Usuniete zadanie z permutacji: ", removedElement)
        print("Nowa permutacja: ", newPermutation)
        print("Spoznienie w nowej permutacji: ", delay)
        return newPermutation

    def secondSA(self, permutation, maxIteration, tmax, tmin, alpha, path):

        #permutation = self.removeTask(self.bestPermutation, path)
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
        u, Sj, Cj, Tj, self.delaySA = self.makeSchedule(permutation, path)
        print("Suma spoznien dla nowej permutacji po SA: ", self.delaySA)

        return permutation

    def removeTask(self, currentPermutation, path):
        u, Sj, Cj, Tj, suma_spoznien = self.makeSchedule(currentPermutation, path)
        print("Czasy zakończeń: ", Cj)
        print("Spoznienia poszczegolnych zadań: ", Sj)
        for i in range(len(currentPermutation)):
            Cj[i] = np.inf

        #print("Obecnie najlepsza permutacja: ", currentPermutation)
        #print("Suma spóźnień przed: ", suma_spoznien)
        #print("Lista spożnien: ", Tj)
        #maxDelay = max(Tj)
        #print("Usunięta wartość: ", maxDelay)
        #index = Tj.index(maxDelay)
        #index = Tj[2]
        #print("Usunięta wartość: ", index)
        #print("Usunięty zadanie nr: ", index)
        #newPermutation = del currentPermutation[0]
        newPermutation = np.delete(currentPermutation, currentPermutation[0])
        print("Permutacja po zmianie: ", newPermutation)
        # filename = "daneAlg\\dane25_4.csv"
        # with open(filename, 'r') as file:
        #     rows = list(csv.reader(file))
        #     del rows[index]
        # with open(filename, 'w',newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerows(rows)
        #u1, Sj1, Cj1, Tj1, sumDelay = self.makeSchedule(newPermutation,path)
        #print("Suma spoznien po zmianie permutacji: ", sumDelay)
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


