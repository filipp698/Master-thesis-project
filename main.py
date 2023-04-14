import numpy as np
import Data
import Parse
import ReadData

# ścieżki do plików testowych
pathData = 'Dane\\dane_moje.txt'

#inicjalizacja obiektu i wczytanie danych
data = Parse.Parse()
data.parse_TL()

#wczytywanie przeparsowanych danych i zaimplementowanie ich do algorytmu
#alg = ReadData.ReadData()
#alg.wykonaj_algorytm(pathData)