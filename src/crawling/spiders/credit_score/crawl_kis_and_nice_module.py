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
            ex_dic["corp"] = (
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

            print(ex_dic["corp"], "is done.")

        except:
            pass

    print("cnt : ", len(ex_list))

    ex_df = pd.DataFrame(ex_list)

    return ex_df


# preprocess module
def kis_preprocess(data):
    # 불필요한 컬럼 제거
    drop = data.drop("evaluate_type", axis=1)

    # 정렬
    sorted = drop.sort_values(["corp", "month"], ascending=True)

    # 최신만 남겨놓고 제거
    duplicate = sorted.drop_duplicates(subset="corp", keep="last")

    # 재배치
    new_columns = ["corp", "year", "month", "day", "bond_type", "rank"]
    reorder = duplicate.reindex(columns=new_columns)

    return reorder


def nice_preprocess(data):
    # 날짜 생성
    data[["year", "month", "day"]] = data["등급확정일"].str.split(".", expand=True)

    # 불필요한 컬럼 제거
    drop1 = data.drop(data.index[data["현재"] == "취소"])
    drop2 = drop1.drop(
        [
            "회차",
            "상환순위",
            "평정",
            "직전",
            "등급결정일\n(평가일)",
            "등급확정일",
            "Unnamed: 6",
            "Unnamed: 8",
            "발행액(억원)",
        ],
        axis=1,
    )

    # 정렬
    sort = drop2.sort_values(["기업명", "month"])

    # 최신만 남겨놓고 제거
    duplicated = sort.drop_duplicates(subset="기업명", keep="last")

    # 재배치
    new_columns = ["기업명", "year", "month", "day", "종류", "현재"]
    reorder = duplicated.reindex(columns=new_columns)

    # (재), (주) 제거 및 컬럼명 재지정
    rename = reorder.rename(columns={"기업명": "corp", "종류": "bond_type", "현재": "rank"})
    rename["corp"] = rename["corp"].str.replace(r"\(재\)|\(주\)", "", regex=True)

    return rename


# SQL
def import_from_mysql(username, password, host_ip, database_name, desired_table_name):
    import pymysql
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    hostname = f"ec2-{host_ip}.ap-northeast-3.compute.amazonaws.com"

    connection_str = f"mysql+pymysql://{username}:{password}@{hostname}/{database_name}"
    engine = create_engine(connection_str)
    query = f"SELECT * FROM {desired_table_name}"

    df = pd.read_sql(query, engine)

    return df


def export_to_mysql(df, username, password, host_ip, database_name, desired_table_name):
    import pymysql
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    hostname = f"ec2-{host_ip}.ap-northeast-3.compute.amazonaws.com"

    cnx = pymysql.connect(user=username, password=password, host=hostname)
    cursor = cnx.cursor()

    engine = create_engine(
        "mysql+pymysql://{user}:{pw}@{host}/{db}".format(
            user=username, pw=password, db=database_name, host=hostname
        )
    )

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Change df name
        df.to_sql(
            desired_table_name,
            con=engine,
            if_exists="replace",
            index=False,
            chunksize=1000,
        )
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    cursor.close()
    cnx.close()
