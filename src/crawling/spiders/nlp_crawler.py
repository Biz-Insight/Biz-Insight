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


def crawl_JP(list_corp):
    # df = pd.DataFrame()
    df = pd.read_csv("./jobplanet/Jobplanet_review.csv", encoding="utf-8")
    # email 본인 아이디, password 본인 패스워드 입력
    # 리뷰를 남겨서 전체 접근이 가능한 상태여야함
    usr = ""
    pwd = ""
    page = 15  # 마지막 페이지
    driver = webdriver.Chrome("/chromedriver.exe")
    driver.get("https://www.jobplanet.co.kr/users/sign_in?_nav=gb")
    time.sleep(7)

    login_id = driver.find_element_by_css_selector("input#user_email")
    login_id.send_keys(usr)

    login_pwd = driver.find_element_by_css_selector("input#user_password")
    login_pwd.send_keys(pwd)
    login_id.send_keys(Keys.RETURN)

    time.sleep(7)
    for query in list_corp:
        try:
            search_query = driver.find_element_by_css_selector(
                "input#search_bar_search_query"
            )
            search_query.send_keys(query)
            search_query.send_keys(Keys.RETURN)
            time.sleep(7)

            driver.find_element_by_css_selector("a.tit").click()
            time.sleep(7)
            try:
                driver.find_element_by_css_selector("button.btn_close_x_ty1 ").click()
                time.sleep(7)
            except:
                pass

            list_company = []
            list_div = []
            list_cur = []
            list_date = []
            list_stars = []
            list_summery = []
            list_merit = []
            list_disadvantages = []
            list_managers = []

            # 직무/근속여부/일시/요약/평점/장점/단점/경영진에게 바라는 점
            print("\n", query, end=": ")
            for i in range(page):
                # 직무, 근속여부, 일시
                user_info = driver.find_elements_by_css_selector("span.txt1")

                count = int(len(user_info) / 4)
                print(count, end=".")

                for j in range(count):
                    list_company.append(query)

                list_user_info = []

                for j in user_info:
                    list_user_info.append(j.text)

                for j in range(
                    count
                ):  # 한 페이지에 정보 5set씩 나옴. 마지막 페이지는 5개 미만일 수 있으므로 count 변수를 반복횟수로 넣어줌.
                    a = list_user_info[4 * j]
                    list_div.append(a)

                    b = list_user_info[4 * j + 1]
                    list_cur.append(b)

                    c = list_user_info[4 * j + 3]
                    list_date.append(c)

                # 별점
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

                # 요약 정보
                summery = driver.find_elements_by_css_selector("h2.us_label")

                for j in summery:
                    list_summery.append(j.text)

                # 장점, 단점, 경영진에게 바라는 점
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

                # 다음 페이지 클릭 후 for문 진행, 끝 페이지에서 다음 페이지 클릭 안되는 것 대비해서 예외처리 구문 추가

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
            df.to_csv("./jobplanet/Jobplanet_review.csv", encoding="utf-8", index=False)

        except:
            driver.get("https://www.jobplanet.co.kr/job")
            time.sleep(4)
            pass

    driver.close()

    return df


def crawl_B(list_corp):
    df = pd.DataFrame()
    page = 15
    driver = webdriver.Chrome("./chromedriver.exe")
    driver.get("https://www.teamblind.com/kr")
    driver.find_element_by_css_selector("a.btn_signin").click()
    time.sleep(15)
    for company in list_corp:
        print(company)
        list_div = []
        list_cur = []
        list_date = []
        list_stars = []
        list_summary = []
        list_merit = []
        list_disadvantages = []

        for i in range(1, page + 1):
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
        df.to_csv(f"./blind/Blind_review.csv", encoding="utf-8", index=False)
    # driver.close()
    return df


# list_corp = KOSPI_corp()
# JP_data = crawl_JP(list_corp)
# B_data = crawl_B(list_corp)
