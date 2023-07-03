# 모듈화
def selenium_basic_setting():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from fake_useragent import UserAgent

    # 1. 브라우저 옵션 세팅
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument("user-agent={}".format(UserAgent().chrome))

    global driver

    # 2. driver 생성
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    # 3. URL
    # URL = "https://www.kisrating.com/ratings/hot_disclosure.do"

    return driver


def start_end_setting(URL, start_date, end_date):
    from selenium.webdriver.common.by import By
    import requests
    from bs4 import BeautifulSoup

    # 0. 새로고침
    driver.get(URL)

    # 1. 객체지정
    startdt = driver.find_element(By.CSS_SELECTOR, "#startDt")

    enddt = driver.find_element(By.CSS_SELECTOR, "#endDt")

    search_btn = driver.find_element(By.CSS_SELECTOR, "#btnSearch")

    # 3. 실행
    startdt.clear()
    startdt.send_keys(start_date)

    enddt.clear()
    enddt.send_keys(end_date)

    search_btn.click()

    # 4. 길이 구하기
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")

    corp_list = soup.select_one("#debentureList tbody")
    corp_cnt = len(corp_list)


def crawl_kis():
    import pandas as pd
    from selenium.webdriver.common.by import By

    corp_list = driver.find_elements(By.CSS_SELECTOR, "#debentureList > tbody")

    ex_list = []

    for tr in range(5000):
        try:
            ex_dic = {}

            ex_dic["year"] = (
                corp_list[0]
                .find_element(
                    By.CSS_SELECTOR,
                    f"#debentureList > tbody > tr:nth-child({tr}) > td:nth-child(8)",
                )
                .text.split(".")[0]
            )
            ex_dic["month"] = (
                corp_list[0]
                .find_element(
                    By.CSS_SELECTOR,
                    f"#debentureList > tbody > tr:nth-child({tr}) > td:nth-child(8)",
                )
                .text.split(".")[1]
            )
            ex_dic["day"] = (
                corp_list[0]
                .find_element(
                    By.CSS_SELECTOR,
                    f"#debentureList > tbody > tr:nth-child({tr}) > td:nth-child(8)",
                )
                .text.split(".")[2]
            )
            ex_dic["corp_name"] = (
                corp_list[0]
                .find_element(
                    By.CSS_SELECTOR,
                    f"#debentureList > tbody > tr:nth-child({tr}) > td:nth-child(2) > a",
                )
                .text
            )
            ex_dic["bond_type"] = (
                corp_list[0]
                .find_element(
                    By.CSS_SELECTOR,
                    f"#debentureList > tbody > tr:nth-child({tr}) > td:nth-child(3)",
                )
                .text
            )
            ex_dic["evaluate_type"] = (
                corp_list[0]
                .find_element(
                    By.CSS_SELECTOR,
                    f"#debentureList > tbody > tr:nth-child({tr}) > td:nth-child(4)",
                )
                .text
            )
            ex_dic["rank"] = (
                corp_list[0]
                .find_element(
                    By.CSS_SELECTOR,
                    f"#debentureList > tbody > tr:nth-child({tr}) > td:nth-child(7)",
                )
                .text
            )

            ex_list.append(ex_dic)

            print(ex_dic["corp_name"], "is done.")

        except:
            pass

    print("cnt : ", len(ex_list))

    ex_df = pd.DataFrame(ex_list)

    return ex_df
