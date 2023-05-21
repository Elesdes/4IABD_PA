import time
from datetime import datetime, timedelta

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    date = datetime(year=2021, month=4, day=24)
    date_end = datetime(year=2023, month=2, day=18)

    while date != date_end:
        df = pd.DataFrame()
        dic_music = {"titre": [], "artiste": []}
        date = date + timedelta(days=7)
        year = date.year
        date_ = str(str(year) + "{:02d}".format(date.month) + "{:02d}".format(date.day))
        driver.get(
            f"https://lescharts.com/weekchart.asp?cat=s&year={year}&date={date_}"
        )

        elements = driver.find_elements(By.XPATH, "//a[@class='navb']")

        for a in elements:
            texte = a.text.split("\n")
            if len(texte) == 2:
                titre = texte[0]
                artist = texte[1]
                dic_music["titre"].append(titre)
                dic_music["artiste"].append(artist)

        df = pd.DataFrame.from_dict(dic_music)
        df["date"] = str(date).split(" ")[0]
        df.to_csv("musique_fr.csv", mode="a", index=False, header=False)
        print(date)
