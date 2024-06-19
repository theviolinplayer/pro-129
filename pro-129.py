from selenium import webdriver 
from selenium.webdriver.common.by import By  
from bs4 import BeautifulSoup  
import time 
import pandas as pd 

# NASA Exoplanet URL
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

browser = webdriver.Chrome()  
browser.get(START_URL)  

time.sleep(2)  

brown_stars_data = [] 

soup = BeautifulSoup(browser.page_source, "html.parser")
table = soup.find_all("table", class_="wikitable")

t_body = table[2].find("tbody")
table_rows = t_body.find_all("tr")
for row in table_rows:
    table_data = row.find_all("td")
    temp = []

    for data in table_data:
        value = data.text.strip()
        temp.append(value)
    
    brown_stars_data.append(temp)

browser.quit()

constellation = []
distance = []
mass = []
radius = []
for row in brown_stars_data:
    if len(row) > 0:
        constellation.append(row[0])
        distance.append(row[4])
        mass.append(row[7])
        radius.append(row[8])

headers = ["constellation", "distance", "mass", "radius"]

df = pd.DataFrame(list(zip(constellation, distance, mass, radius)), columns=headers)


df.to_csv("brown_stars_csv_file.csv", index_label="id")

brown_dwarfs_df = pd.read_csv("brown_stars_csv_file.csv")

brown_dwarfs_df.dropna(inplace=True)

brown_dwarfs_df['mass'] = brown_dwarfs_df['mass'].astype(float)
brown_dwarfs_df['radius'] = brown_dwarfs_df['radius'].astype(float)

brown_dwarfs_df['radius'] = brown_dwarfs_df['radius'] * 0.102763

brightest_stars_df = pd.read_csv("brightest_stars_csv_file.csv")

merged_df = pd.merge(brown_dwarfs_df, brightest_stars_df, how='inner', on='constellation')

merged_df.to_csv("merged_stars_csv_file.csv", index_label='id')
