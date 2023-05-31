import random
import time
import math
import csv
import numpy as np
from ReadData import ReadData
import matplotlib.pyplot as plt
import matplotlib.cm as cm


class SA(ReadData):
    firstPermutation = np.zeros(3, dtype=int)
    n = 0
    changesOccured = True
    newPermutation = []
    bestDelay = 9999
    bestPermutation = []
    delaySA = 9999
    bestSecondDelay = 9999
    bestSecondPermutation = []
    removedElements = []

    # def __init__(self):
    #     pass

    def createFirstPermutation(self, path):
        _, iloscZamowien, _, _, _, _, _, _, permutation = self.readData(path)
        #self.firstPermutation = self.generateRandomPermutation(permutation)
        self.firstPermutation = permutation
        self.n = iloscZamowien
    def generateRandomPermutation(self, permutation):
        permutation = np.random.permutation(permutation)
        return permutation
    def swap(self, currentTour, i, j):
        newTour = np.copy(currentTour)
        if i <= j:
            partToFlip = np.copy(newTour[i:j + 1])
            newTour[i:j + 1] = np.flip(partToFlip)
        else:
            partToFlip = np.copy(newTour[j:i + 1])
            newTour[j:i + 1] = np.flip(partToFlip)
        return newTour

    def SA(self, initialPermutation, maxIteration, tmax, tmin, alpha, path, option,maxIterSA):
        start1 = time.time()
        temp = tmax
        currentPermutation = initialPermutation
        _, _, _, _, currentDelay = self.makeSchedule(currentPermutation, path)
        self.bestPermutation = currentPermutation
        #z_, _, _, _, self.bestDelay = self.makeSchedule(initialPermutation, path)
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
        u, Sj, Cj, Tj, suma_spoznien = self.makeSchedule(self.bestPermutation, path)
        bestPremutation = self.bestPermutation
        ammountOfIteration = 0
        print("Suma spoznien na początku: ", suma_spoznien)
        print("Najlepsza permutacja: ", self.bestPermutation)
        #print("Lista spoznionych zadań", Tj)
        ## Wyrzucanie każdego z zadań pojedynczo
        if option == 1:
            while self.delaySA != 0:
                permutationSA = self.findLongestTasks(bestPremutation, path)
                SA2 = self.secondSA(permutationSA, maxIterSA, tmax, tmin, alpha, path)
                bestPremutation = SA2
                ammountOfIteration += 1
                if self.delaySA == 0:
                    print("Spoznienie rowne jest 0")
            print("Permutacja ostateczna: ", SA2)
            print("Dlugosc ostatecznej premutacji: ", len(SA2))
            print("Ilosc iteracji petli while: ", ammountOfIteration)
        ## Wyrzucenie zadań przeterminowanych
        if option == 2:
            while self.delaySA != 0:
                permutationSA = self.findLongestDelayedTask(bestPremutation, path)
                SA2 = self.secondSA(permutationSA, maxIterSA, tmax, tmin, alpha, path)
                bestPremutation = SA2
                ammountOfIteration += 1
                if self.delaySA == 0:
                    print("Spoznienie rowne jest 0")
            print("Permutacja ostateczna: ", SA2)
            print("Dlugosc ostatecznej premutacji: ", len(SA2))
            #print("Ilosc iteracji petli while: ", ammountOfIteration)
        end1 = time.time()
        self.durationSA = end1 - start1
        self.bestPermutation = SA2
        #print("Czas trwania obliczeń: " ,round(self.durationSA,2), "[s]")

        return self.bestPermutation

    def findLongestTasks(self, permutation, path):
        lista_spoznien = []
        for i in range(0,len(permutation)):
            _, _, _, _, spoznienia = self.makeScheduleInfinity(permutation, i, path)
            lista_spoznien.append(spoznienia)
        minDelay = min(lista_spoznien)  # wartość spoźnienia, które daje najwieksze efekty
        index = lista_spoznien.index(minDelay)
        removedElement = permutation[index]
        self.removedElements.append(removedElement)
        newPermutation = np.delete(permutation, index)
        _, _, _, _, self.delaySA = self.makeSchedule(newPermutation, path)
        print("Lista spoznien dla danych zadan: ", lista_spoznien)
        print("Index wyrzuconej wartości: ", index)
        print("Usuniete zadanie z permutacji: ", removedElement)
        print("Nowa permutacja: ", newPermutation)
        print("Aktualna ilosc zadan: ", len(newPermutation))
        print("Spoznienie w nowej permutacji: ", self.delaySA)
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
        self.removedElements.append(removedElement)
        newPermutation = np.delete(permutation, index)
        _, _, _, _, self.delaySA = self.makeSchedule(newPermutation, path)
        print("Lista przeterminowanych zadan: ", lista_spoznien)
        print("Index wyrzuconej wartości: ", index)
        print("Usuniete zadanie z permutacji: ", removedElement)

        print("Nowa permutacja: ", newPermutation)
        print("Aktualna ilosc zadan: ", len(newPermutation))
        print("Spoznienie w nowej permutacji: ", self.delaySA)
        return newPermutation

    def secondSA(self, permutation, maxIteration, tmax, tmin, alpha, path):
        temp = tmax
        _, _, _, _, currentBestLen = self.makeSchedule(permutation, path)
        self.bestSecondPermutation = permutation
        self.bestSecondDelay = currentBestLen
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
                if newLen < self.bestSecondDelay:
                    self.bestSecondDelay = newLen
                    self.bestSecondPermutation = newPermutation
                delta = newLen - currentBestLen
                probabilityOfAcceptance = random.uniform(0, 1)
                if delta < 0:
                    permutation = newPermutation
                else:
                    probability = math.exp(-delta / temp)
                    if probability >= probabilityOfAcceptance:
                        permutation = newPermutation
                end_iteration = time.time()
                self.durationOfIteration = end_iteration - start_interation
                # print("Czas trwania iteracji wynosi: ", durationOfIteration)
            temp *= alpha
        _, _, _, _, self.delaySA = self.makeSchedule(self.bestSecondPermutation, path)
        print("Suma spoznien dla nowej permutacji po SA: ", self.delaySA)

        return self.bestSecondPermutation

    def result(self,path,pathWynik):
        u, Sj, Cj, Tj, delaySA = self.makeSchedule(self.bestPermutation, path)
        #print("Lista urządzeń", u)
        with open(pathWynik, "w") as file:
            for i in range(len(Sj)):
                file.write("Zad " + str(self.bestPermutation[i]) + ": ")
                nr = int(self.bestPermutation[i])
                file.write(str(Sj[i]) + " ")
                file.write(str(Cj[i]) + " : ")
                file.write(str(u[nr-1]) + "\n")
            file.write('Suma spoznien wynosi: ' + str(delaySA) + '\n')
            file.write('Ilosc zadan zrealizowanych: ' + str(len(self.bestPermutation)) + '\n')
            file.write('Ostateczna premutacja: ' + str(self.bestPermutation) + '\n')
            file.write('Czas trwania iteracji wynosi: ' + str(self.durationOfIteration) + " [s]" + '\n')
            file.write('Czas trwania algorytmu: ' + str(round(self.durationSA, 3)) + " [s]" + '\n')

    def result_system(self,path,pathWynik):
        u, Sj, Cj, Tj, delaySA = self.makeSchedule(self.bestPermutation, path)
        #print("Lista urządzeń", u)
        # zamiana kluczy i wartości ze słownika słowo na wartość-klucz
        dictionary = {str(value): key for key, values in self.slownik2.items() for value in values}
        # zamiana listy urządzeń na format z nowego słownika (odwzorowanie)
        u_reparse = [[dictionary[str(element)] for element in group] for group in u]
        #print(u_reparse)
        sortedPermutation = sorted(self.bestPermutation, key=int)
        #print(self.bestPermutation)
        #print(sortedPermutation)
        bestPremutation = self.bestPermutation.tolist()
        tasks = []
        timesOfStart = []
        timesOfFinish = []

        with open(pathWynik, "w") as file:
            for i in range(len(Sj)):
                file.write("Zad nr " + str(sortedPermutation[i]) + ":" + "\n")
                tasks.append("Zad " + str(sortedPermutation[i]))
                nr_zad = int(sortedPermutation[i])
                index = bestPremutation.index(nr_zad)
                file.write("Rozpoczęcie zadania: " + str(Sj[index]) + ", ")
                file.write("Koniec zadania: " + str(Cj[index]) + "\n")
                timesOfStart.append(int(Sj[index]))
                timesOfFinish.append(int(Cj[index]))
                file.write("Lista niezbędnych zasobów: " + str(u_reparse[nr_zad-1]) + "\n")
            file.write('\n' + 'Liczba możliwych zadań do zrealizowania: ' + str(len(self.bestPermutation)) + '\n')
            file.write('Niezrealizowane zadania: ' + str(self.removedElements) + '\n')
        #print("Zadania", tasks)
        #print("Start", timesOfStart)
        #print("Koniec", timesOfFinish)
        # Tworzenie wykresu Gantta
        if len(tasks) > 30:
            fig = plt.figure(figsize=(8,8))
        else:
            fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        #fig, ax = plt.subplots()
        cmap = cm.get_cmap('rainbow', len(tasks))
        #custom_colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'cyan', 'magenta', 'gray', 'brown']
        for i in range(len(tasks)):
            ax.broken_barh([(timesOfStart[i], timesOfFinish[i] - timesOfStart[i])], (10 * i, 7), facecolors=cmap(i))

        # Konfiguracja osi
        ax.set_ylim(0, 10 * len(tasks))
        ax.set_xlim(0, max(timesOfFinish))
        ax.set_xlabel('Czas [tyg]')
        #ax.set_ylabel('Numer zadania')
        ax.set_title('Wykres Gantta')
        #ax.yaxis.set_tick_params(labelsize=8)
        ax.set_yticks([10 * i + 5 for i in range(len(tasks))])
        ax.set_yticklabels(tasks)
        plt.show()




