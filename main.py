import numpy as np
import Data
import Parse
import ReadData
import TabuSearch
import SA

# ścieżki do plików testowych
pathOrder = "daneTestowe\\dane50.csv"
pathZasoby = "Dane\\zasoby.csv"
pathData = "Dane\\dane_sparsowane.txt"
pathWynik = "Dane\\wyniki.txt"

#inicjalizacja obiektu i wczytanie danych
data = Parse.Parse()
data.parse_TL(pathOrder,pathZasoby,pathData)

#wczytywanie przeparsowanych danych i zaimplementowanie ich do algorytmu wyznaczającego harmonogram
# alg = ReadData.ReadData()
# alg.zapisz_wynik(pathWynik)

# Algorytm SA
symulowane = SA.SA(pathData)
symulowane.createFirstTour(pathData)
# określenie max liczby interacji dla SA
maxIterationNumber = 10**4
# określenie max temperatury dla SA
maxTemperature = 45
symulowane.SA(maxIterationNumber, maxTemperature,pathData)

#Dane do algorytmu Tabu Search
# lengthOfTabu = 7
# option = "swap"
# iterationNumber = 100
# cycleNumberMax = 5
# isReactiveTabu = False
# reactiveInterval = 50
#
# tabu = TabuSearch.TabuSearch(pathData)
# tabu.execute(tabu.firstPermutation, lengthOfTabu, option, iterationNumber, cycleNumberMax, isReactiveTabu, reactiveInterval)
# print("-------------------")
# print("First permutation: " + str(tabu.firstPermutation))
# print("Suma spóźnien dla pierwszej permutacji: " + str(tabu.suma_kar))
# print("-------------------")
# print("Best permutation: " + str(tabu.bestPermutation))
# print("Suma spóźniej dla najlepszej permutacji: " + str(tabu.bestDistance))
# print("-------------------")