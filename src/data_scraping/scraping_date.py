import contextlib
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def process_data():
    df = pd.read_csv("all_musique_rv_tom.csv", sep=",")
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.discogs.com/fr/")
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
    ).click()
    for index, row in df.iterrows():
        print(index)
        inputElement = driver.find_element(by=By.ID, value="search_q")
        artists = row["ARTISTE"]
        featuring_in_artist = row["ARTISTE"]
        to_replace_by_and_word = [
            "featuring",
            "Featuring",
            "featuring.",
            "Featuring.",
            "FEATURING",
            "FEATURING.",
            "ft",
            "ft.",
            "Ft",
            "Ft.",
            "FT",
            "FT.",
            "feat",
            "feat.",
            "Feat",
            "Feat.",
            "FEAT",
            "FEAT.",
        ]
        for word in to_replace_by_and_word:
            if word in featuring_in_artist:
                artists = featuring_in_artist.replace(word, "&")
                break
        song = f'{artists} {row["TITRE"]}'
        print(artists)
        inputElement.send_keys(song)
        inputElement.send_keys(Keys.ENTER)
        list_card = driver.find_elements(by=By.XPATH, value="//li[@role = 'listitem']")

        found = False
        for l_card in list_card:
            card = l_card.text
            """
            print(l_card)
            print('-----------')
            print(card)
            print(len(card.split("\n")))
            """
            if len(card.split("\n")) == 2:
                aria_label = str(card.split("\n")[1] + " - " + card.split("\n")[0])
                time.sleep(2)
                with contextlib.suppress(Exception):
                    WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located(
                            (By.XPATH, f'//a[@aria-label = "{aria_label}"]')
                        )
                    ).click()
                    found = True
                    break
        if not found:
            df_data_row = {
                "TITRE": [row["TITRE"]],
                "ARTISTE": [artists],
                "LASTE_DATE_IN_TOP": [row["LASTE_DATE_IN_TOP"]],
            }
            df_data_row = pd.DataFrame(df_data_row)
            df_data_row.to_csv(
                "not_done_impaire_asc.csv", mode="a", index=False, header=False
            )
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "header_logo"))
            ).click()
        else:
            list_elements = driver.find_elements(by=By.XPATH, value="//tr")
            genre = ""
            style = ""
            annee = ""
            time.sleep(2)
            for element in list_elements:
                value_element = element.text
                if value_element.startswith("Genre: "):
                    genre = value_element.split(": ")[1]
                elif value_element.startswith("Style: "):
                    style = value_element.split(": ")[1]
                elif value_element.startswith("Année: "):
                    annee = value_element.split(": ")[1]
                elif value_element.startswith("Sortie: "):
                    annee = value_element.split(": ")[1].strip()
            try:
                if annee == "" or (
                    int(row["LASTE_DATE_IN_TOP"].split("-")[0]) < int(annee)
                ):
                    annee = row["LASTE_DATE_IN_TOP"].split("-")[0]
            except ValueError:
                annee = list(annee)
                annee = annee[-4:]
                annee = int("".join(annee))
                if annee == "" or (int(row["LASTE_DATE_IN_TOP"].split("-")[0]) < annee):
                    annee = row["LASTE_DATE_IN_TOP"].split("-")[0]
            print(song, "---", aria_label, "---", genre, "---", style, "---", annee)
            df_data_row = {
                "TITRE": [row["TITRE"]],
                "ARTISTE": [artists],
                "LASTE_DATE_IN_TOP": [annee],
            }
            df_data_row = pd.DataFrame(df_data_row)
            df_data_row.to_csv(
                "donees_impaire_asc.csv", mode="a", index=False, header=False
            )
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "discogs-logo"))
            ).click()


if __name__ == "__main__":
    process_data()
