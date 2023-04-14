import numpy as np
import Data
import Parse
import ReadData

# ścieżki do plików testowych
pathOrder = "daneTestowe\\dane100_1.csv"
pathZasoby = "Dane\\zasoby.csv"
pathData = "Dane\\dane_sparsowane.txt"

#inicjalizacja obiektu i wczytanie danych
data = Parse.Parse()
data.parse_TL(pathOrder,pathZasoby,pathData)

#wczytywanie przeparsowanych danych i zaimplementowanie ich do algorytmu
alg = ReadData.ReadData()
alg.wykonaj_algorytm(pathData)