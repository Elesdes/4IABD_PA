from datetime import datetime
from datetime import timedelta

import pandas as pd
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

if __name__ == '__main__':
    df_bill1 = pd.read_csv("musique.csv")
    df_bill2 = pd.read_csv("musique2.csv")
    df_top50 = pd.read_csv("musique_fr.csv")
    df = pd.concat([df_bill1, df_bill2, df_top50])
    df = df.drop_duplicates("titre", keep='first')
    df = df.rename(columns={"date": "LASTE_DATE_IN_TOP", "titre": "TITRE", "artiste": "ARTISTE"})
    df = df.sort_values(by=['LASTE_DATE_IN_TOP'], ascending=False) #
    df = df.iloc[:12516]
    df.to_json("all_musique_rv_erwan.json", orient='records')
    df.to_csv("all_musique_rv_erwan.csv", index=False, header=True)
