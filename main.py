import numpy as np
import Data

# ścieżki do plików testowych
pathOrder = "daneTestowe\\daneOrder.txt"
pathRU = "daneTestowe\\daneRU.txt"
pathTL = "daneTestowe\\daneTL.txt"
#inicjalizacja obiektu i wczytanie danych
dane = Data.Data()
dane.importOrder(pathOrder)
dane.importRU(pathRU)
dane.importTL(pathTL)