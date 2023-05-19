import time
import numpy as np
import Data
import Parse
import ReadData
import TabuSearch
import SA

# ścieżki do plików testowych
pathOrder = "daneTestowe\\dane25_2.csv"
pathZasoby = "Dane\\zasoby.csv"
pathData = "Dane\\dane_sparsowane.txt"
pathWynik = "Wyniki\\wyniki_" + pathOrder[-12:-4] + ".txt"
pathWynikTS = "Wyniki\\wyniki_TS_" + pathOrder[-12:-4] + "_"
pathWynikSA = "Wyniki\\wyniki_SA_" + pathOrder[-12:-4] + ".txt"

#inicjalizacja obiektu i wczytanie danych
data = Parse.Parse()
data.parseTL(pathOrder, pathZasoby, pathData)

#wczytywanie przeparsowanych danych i zaimplementowanie ich do algorytmu wyznaczającego harmonogram
# alg = ReadData.ReadData(pathData)
# alg.makeSchedule(alg.firstPermutation, pathData)
# alg.saveResults(pathData,pathWynik)

# # Algorytm SA
SA_start = time.time()
symulowane = SA.SA(pathData)
symulowane.createFirstPermutation(pathData)
# określenie parametrów dla SA
maxIterationNumber = 25
maxTemperature = 1000
minTemperature = 0.1
alpha = 0.98
symulowane.SA(symulowane.firstPermutation, maxIterationNumber, maxTemperature, minTemperature, alpha, pathData)
#symulowane.removeTask(symulowane.bestPermutation,pathData)
#symulowane.SA2(maxIterationNumber, maxTemperature, minTemperature, alpha, pathData)
# #symulowane.removeTask(pathData)
# SA_end = time.time()
# duration_SA = SA_end - SA_start
# print("Czas trwania SA: ", round(duration_SA,3), "[s]")

#Dane do algorytmu Tabu Search
# lengthOfTabu = 7
# option = "insert"
# iterationNumber = 100
# cycleNumberMax = 5
# isReactiveTabu = False
# reactiveInterval = 50
#
# tabu_start = time.time()
# tabu = TabuSearch.TabuSearch(pathData)
# tabu.execute(tabu.firstPermutation, lengthOfTabu, option, iterationNumber, cycleNumberMax, isReactiveTabu, reactiveInterval,pathData, pathWynikTS)
# tabu_end = time.time()
# duration_tabu = tabu_end - tabu_start
# print("-------------------")
# print("First permutation: " + str(tabu.firstPermutation))
# print("Suma spóźnien dla pierwszej permutacji: " + str(tabu.suma_kar))
# print("-------------------")
# print("Best permutation: " + str(tabu.bestPermutation))
# print("Suma spóźnien dla najlepszej permutacji: " + str(tabu.bestDelay))
# print("-------------------")
# print("Czas trwania Tabu: ", round(duration_tabu,2), "[s]")

# np.savetxt("funkcja_celu_best.txt", tabu.permutationHistoryGlobal, comments = "", fmt = '%f')
# np.savetxt("funkcja_celu_local_best.txt", tabu.permutationHistoryLocal, comments = "", fmt = '%f')