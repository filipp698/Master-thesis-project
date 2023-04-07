#import numpy as np
import Data
import Parse
import ReadData

# ścieżki do plików testowych
pathOrder = "Dane\\dane_order.csv"
pathData = 'Dane\\data_prog.txt'
#inicjalizacja obiektu i wczytanie danych
data = Parse.Parse()
data.importOrder(pathOrder)
#wcztywanie przeparsowanych danych i zaimplementowanie ich do algorytmu
alg = ReadData.ReadData()
alg.wykonaj_algorytm(pathData)