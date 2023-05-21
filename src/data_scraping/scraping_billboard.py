from datetime import datetime
from datetime import timedelta

import pandas as pd
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    date_end = datetime(year=1973, month=1, day=6)
    date = datetime(year=2018, month=6, day=9)

    while date != date_end:
        df = pd.DataFrame()
        dic_music = {"titre": [], "artiste": []}
        date = (date + timedelta(days=-7))
        date_ = str(date).split(" ")[0]

        driver.get(f"https://www.billboard.com/charts/hot-100/{date_}/")
        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click()
        except:
            pass
        elements = driver.find_elements(By.XPATH, "//li[@class='lrv-u-width-100p']")
        for a in elements:
            titre = a.find_elements(by=By.TAG_NAME, value='h3')
            artist = a.find_elements(by=By.TAG_NAME, value='span')
            if len(titre) & len(artist) == 1:
                dic_music["titre"].append(titre[0].text)
                dic_music["artiste"].append(artist[0].text)

        df = pd.DataFrame.from_dict(dic_music)
        df['date'] = date_
        df.to_csv("musique2.csv", mode='a', index=False, header=False)
        print(date)