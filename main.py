import numpy as np
import Data
import Parse

# ścieżki do plików testowych
pathOrder = "Dane\\dane_order.csv"
pathRU = "Dane\\dane_radia.csv"
pathTL = "Dane\\dane_testlines.csv"
#inicjalizacja obiektu i wczytanie danych
data = Parse.Parse()
data.importOrder(pathOrder)
#data.importTL(pathTL)
#data.importRU(pathRU)