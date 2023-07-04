# Basic Settings
from crawl_kis_module import *
import pandas as pd

URL = "https://www.kisrating.com/ratings/hot_disclosure.do"

driver = selenium_basic_setting()

# 2019
start_end_setting(URL=URL, start_date="2018.03.31", end_date="2018.09.29")

kis_2019 = crawl_kis()
kis_2019.to_csv("kis_2019.csv", encoding="cp949")

# 2020
start_end_setting(URL=URL, start_date="2019.03.31", end_date="2019.09.29")

kis_2020 = crawl_kis()
kis_2020.to_csv("kis_2020.csv", encoding="cp949")

# 2021
start_end_setting(URL=URL, start_date="2020.03.31", end_date="2020.09.29")

kis_2021 = crawl_kis()
kis_2021.to_csv("kis_2021.csv", encoding="cp949")

# 2022
start_end_setting(URL=URL, start_date="2021.03.31", end_date="2021.09.29")

kis_2022 = crawl_kis()
kis_2022.to_csv("kis_2022.csv", encoding="cp949")

# 2023
start_end_setting(URL=URL, start_date="2022.03.31", end_date="2022.09.29")

kis_2023 = crawl_kis()
kis_2023.to_csv("kis_2023.csv", encoding="cp949")

# quit
driver.quit()
