# Basic Settings
from crawl_kis_and_nice_module import *
import pandas as pd

########
# KIS  #
########

URL = "https://www.kisrating.com/ratings/hot_disclosure.do"

driver = selenium_basic_setting()

# 2019
start_end_setting(URL=URL, start_date="2019.03.17", end_date="2020.03.16")
kis_2019 = crawl_kis()

# 2020
start_end_setting(URL=URL, start_date="2020.03.17", end_date="2021.03.16")
kis_2020 = crawl_kis()

# 2021
start_end_setting(URL=URL, start_date="2021.03.17", end_date="2022.03.16")
kis_2021 = crawl_kis()

# 2022
start_end_setting(URL=URL, start_date="2022.03.17", end_date="2023.03.16")
kis_2022 = crawl_kis()

# 2023
start_end_setting(URL=URL, start_date="2023.03.17", end_date="2023.07.10")
kis_2023 = crawl_kis()

# preprocessing
processed_kis_2019 = kis_preprocess(data=kis_2019)
processed_kis_2020 = kis_preprocess(data=kis_2020)
processed_kis_2021 = kis_preprocess(data=kis_2021)
processed_kis_2022 = kis_preprocess(data=kis_2022)
processed_kis_2023 = kis_preprocess(data=kis_2023)

# output
processed_kis_2019.to_csv("./kis_2019.csv", encoding="cp949", index=False)
processed_kis_2020.to_csv("./kis_2020.csv", encoding="cp949", index=False)
processed_kis_2021.to_csv("./kis_2021.csv", encoding="cp949", index=False)
processed_kis_2022.to_csv("./kis_2022.csv", encoding="cp949", index=False)
processed_kis_2023.to_csv("./kis_2023.csv", encoding="cp949", index=False)

########
# NICE #
########

# import csv
nice_2019 = pd.read_excel("./nice_2019_raw.xls", skiprows=1).drop(0)
nice_2020 = pd.read_excel("./nice_2020_raw.xls", skiprows=1).drop(0)
nice_2021 = pd.read_excel("./nice_2021_raw.xls", skiprows=1).drop(0)
nice_2022 = pd.read_excel("./nice_2022_raw.xls", skiprows=1).drop(0)
nice_2023 = pd.read_excel("./nice_2023_raw.xls", skiprows=1).drop(0)

# preprocessing
processed_nice_2019 = nice_preprocess(data=nice_2019)
processed_nice_2020 = nice_preprocess(data=nice_2020)
processed_nice_2021 = nice_preprocess(data=nice_2021)
processed_nice_2022 = nice_preprocess(data=nice_2022)
processed_nice_2023 = nice_preprocess(data=nice_2023)

# output
processed_nice_2019.to_csv("./nice_2019.csv", encoding="cp949", index=False)
processed_nice_2020.to_csv("./nice_2020.csv", encoding="cp949", index=False)
processed_nice_2021.to_csv("./nice_2021.csv", encoding="cp949", index=False)
processed_nice_2022.to_csv("./nice_2022.csv", encoding="cp949", index=False)
processed_nice_2023.to_csv("./nice_2023.csv", encoding="cp949", index=False)
