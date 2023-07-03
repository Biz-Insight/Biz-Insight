from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import re


def KOSPI_corp():
    list_corp = pd.read_csv("상장법인목록.csv")["회사명"].tolist()
    return list_corp


def JB_review(df, driver, company):
    list_company = []
    list_div = []
    list_cur = []
    list_date = []
    list_stars = []
    list_summery = []
    list_merit = []
    list_disadvantages = []
    list_managers = []

    print("\n", company, end=": ")
    for i in range(15):
        user_info = driver.find_elements_by_css_selector("span.txt1")

        count = int(len(user_info) / 4)
        print(count, end=".")

        for j in range(count):
            list_company.append(company)

        list_user_info = []

        for j in user_info:
            list_user_info.append(j.text)

        for j in range(count):
            a = list_user_info[4 * j]
            list_div.append(a)

            b = list_user_info[4 * j + 1]
            list_cur.append(b)

            c = list_user_info[4 * j + 3]
            list_date.append(c)

        stars = driver.find_elements_by_css_selector("div.star_score")
        for j in stars:
            a = j.get_attribute("style")
            if a[7:9] == "20":
                list_stars.append("1점")
            elif a[7:9] == "40":
                list_stars.append("2점")
            elif a[7:9] == "60":
                list_stars.append("3점")
            elif a[7:9] == "80":
                list_stars.append("4점")
            else:
                list_stars.append("5점")

        summery = driver.find_elements_by_css_selector("h2.us_label")

        for j in summery:
            list_summery.append(j.text)

        list_review = []
        review = driver.find_elements_by_css_selector("dd.df1")
        for j in review:
            list_review.append(j.text)
        for j in range(count):  # 페이지당 5set
            a = list_review[3 * j]
            list_merit.append(a)

            b = list_review[3 * j + 1]
            list_disadvantages.append(b)

            c = list_review[3 * j + 2]
            list_managers.append(c)

        if count < 5:
            break

        try:
            driver.find_element_by_css_selector("a.btn_pgnext").click()
            time.sleep(15)
        except:
            pass

    total_data = pd.DataFrame()
    total_data["회사"] = pd.Series(list_company)
    total_data["날짜"] = pd.Series(list_date)
    total_data["직무"] = pd.Series(list_div)
    total_data["재직여부"] = pd.Series(list_cur)
    total_data["별점"] = pd.Series(list_stars)
    total_data["요약"] = pd.Series(list_summery)
    total_data["장점"] = pd.Series(list_merit)
    total_data["단점"] = pd.Series(list_disadvantages)
    total_data["경영진에게 바라는 점"] = pd.Series(list_managers)
    df = pd.concat([df, total_data])
    df.to_csv("./jobplanet/Jobplanet_review_0701.csv", encoding="utf-8", index=False)

    return df


def JB_star(df, driver, company):
    try:
        star = driver.find_element_by_css_selector("span.rate_point")
        stars = driver.find_elements(By.XPATH, '//*[@class="txt_point"]')
        pies = driver.find_elements(By.XPATH, '//*[@class="rate_pie_set"]')
        corp_dict = {
            "회사": company,
            "잡플래닛평점": float(star.text),
            "복지 및 급여": float(stars[0].text),
            "업무와 삶의 균형": float(stars[1].text),
            "사내문화": float(stars[2].text),
            "승진 기회 및 가능성": float(stars[3].text),
            "경영진": float(stars[4].text),
            "기업추천율": float(re.sub(r"[^0-9]", "", pies[0].text)) / 100,
            "CEO지지율": float(re.sub(r"[^0-9]", "", pies[1].text)) / 100,
            "성장가능성": float(re.sub(r"[^0-9]", "", pies[2].text)) / 100,
        }
        df = pd.concat([df, pd.DataFrame([corp_dict])])
        df.to_csv("./jobplanet/Jobplanet_star_0701.csv", encoding="utf-8", index=False)
    except:
        pass
    return df


def crawl_JP(list_corp, mode):
    driver = webdriver.Chrome("C:/Users/junel/Downloads/chromedriver.exe")
    driver.get("https://www.jobplanet.co.kr/users/sign_in?_nav=gb")
    time.sleep(7)
    # email 본인 아이디, password 본인 패스워드 입력
    # 리뷰를 남겨서 전체 접근이 가능한 상태여야 함
    usr = "junelalala@ewhain.net"
    pwd = "Jobfkffk59!"
    login_id = driver.find_element_by_css_selector("input#user_email")
    login_id.send_keys(usr)

    login_pwd = driver.find_element_by_css_selector("input#user_password")
    login_pwd.send_keys(pwd)
    login_id.send_keys(Keys.RETURN)

    time.sleep(7)
    for company in list_corp:
        try:
            search_query = driver.find_element_by_css_selector(
                "input#search_bar_search_query"
            )
            search_query.send_keys(company)
            search_query.send_keys(Keys.RETURN)
            time.sleep(7)

            driver.find_element_by_css_selector("a.tit").click()
            time.sleep(7)
            try:
                driver.find_element_by_css_selector("button.btn_close_x_ty1 ").click()
                time.sleep(7)
            except:
                pass

            if mode == "JB_review":
                # df = pd.DataFrame()
                df = pd.read_csv("./jobplanet/Jobplanet_review.csv", encoding="utf-8")
                df = JB_review(df, driver, company)

            elif mode == "JB_star":
                # df = pd.DataFrame()
                df = pd.read_csv(
                    "./jobplanet/Jobplanet_star_0701.csv", encoding="utf-8"
                )
                df = JB_star(df, driver, company)

        except:
            driver.get("https://www.jobplanet.co.kr/job")
            time.sleep(4)
            pass

    driver.close()

    return df


def B_star(df, driver, company):
    try:
        driver.get(f"https://www.teamblind.com/kr/company/{company}/reviews?")
        time.sleep(5)

        if driver.find_element_by_css_selector("section.not-found"):
            # print("NOT FOUND")
            driver.find_element_by_css_selector("button.btn-srch").click()
            time.sleep(5)
            search = driver.find_element_by_css_selector("input#keyword")
            search.send_keys(company)
            search.send_keys(Keys.RETURN)
            time.sleep(5)
            driver.find_element(By.XPATH, '//*[@class="dtl"]/ul/li/a').click()
            time.sleep(5)

        star = float(
            driver.find_elements(By.XPATH, '//*[@class="star"]')[0].text.split("\n")[-1]
        )
        stars = driver.find_elements(By.XPATH, '//*[@class="star"]')
        bind_dict = {
            "회사": company,
            "블라인드평점": star,
            "커리어 향상": float(stars[6].text),
            "업무와 삶의 균형": float(stars[7].text),
            "급여 및 복지": float(stars[8].text),
            "사내 문화": float(stars[9].text),
            "경영진": float(stars[10].text),
        }
        df = pd.concat([df, pd.DataFrame([bind_dict])])
        df.to_csv(f"./blind/Blind_star_0701.csv", encoding="utf-8", index=False)
    except:
        pass
    return df


def B_review(df, driver, company):
    list_div = []
    list_cur = []
    list_date = []
    list_stars = []
    list_summary = []
    list_merit = []
    list_disadvantages = []

    for i in range(1, 16):
        try:
            print(i, "page")
            driver.get(
                f"https://www.teamblind.com/kr/company/{company}/reviews?page={i}"
            )
            time.sleep(5)

            reviews = driver.find_elements(By.XPATH, '//*[@class="parag"]/p/span')
            if len(reviews) == 0:
                break

            # if == 1:
            #    total_star = driver.find_element(By.XPATH, '//*[@id="wrap"]/section/div/div/div[2]/div/div/div/div/section[1]/div/div[1]/div[1]/strong').text

            cnt = 0
            for review in reviews:
                if cnt == 0:
                    list_merit.append(review.text.replace("\n", ""))
                    cnt += 1
                elif cnt == 1:
                    list_disadvantages.append(review.text.replace("\n", ""))
                    cnt = 0

            # Rating Score
            rating = driver.find_elements(By.XPATH, '//*[@class="rating"]/strong')
            for star in rating:
                list_stars.append(float(star.text.split("\n")[-1]))
            # Title
            titles = driver.find_elements(By.CLASS_NAME, "rvtit")
            for title in titles:
                list_summary.append(title.text[1:-1])

            auths = driver.find_elements(By.CLASS_NAME, "auth")
            for auth in auths:
                info = auth.text.split(" · ")
                list_cur.append(info[0][-3:])
                list_div.append(info[-1].split(" - ")[0])
                list_date.append(info[-1].split(" - ")[1])

        except:
            pass

    total_data = pd.DataFrame()
    total_data["회사"] = [company] * len((list_date))
    total_data["날짜"] = pd.Series(list_date)
    total_data["직무"] = pd.Series(list_div)
    total_data["재직여부"] = pd.Series(list_cur)
    total_data["별점"] = pd.Series(list_stars)
    total_data["요약"] = pd.Series(list_summary)
    total_data["장점"] = pd.Series(list_merit)
    total_data["단점"] = pd.Series(list_disadvantages)
    df = pd.concat([df, total_data])
    df.to_csv(f"./blind/Blind_review0701.csv", encoding="utf-8", index=False)
    return df


def crawl_B(list_corp, mode):
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://www.teamblind.com/kr")
    driver.find_element_by_css_selector("a.btn_signin").click()
    time.sleep(15)
    for company in list_corp:
        print(company)
        if mode == "B_review":
            # df = pd.DataFrame()
            df = pd.read_csv("./blind/Blind_review.csv", encoding="utf-8")
            df = B_review(df, driver, company)
        elif mode == "B_star":
            # df = pd.DataFrame()
            df = pd.read_csv("./blind/Blind_star_0701.csv", encoding="utf-8")
            df = B_star(df, driver, company)
    return df


# list_corp = KOSPI_corp()
# JP_data = crawl_JP(list_corp)
# B_data = crawl_B(list_corp)
