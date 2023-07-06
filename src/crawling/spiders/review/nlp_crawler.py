from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re
import warnings

warnings.filterwarnings(action="ignore")


def JP_review(df, driver, corp, stock_code):
    list_company = []
    list_code = []
    list_div = []
    list_cur = []
    list_date = []
    list_stars = []
    list_summary = []
    list_merit = []
    list_disadvantages = []
    list_managers = []

    print("\n", corp, end=": ")
    for p in range(15):
        user_info = driver.find_elements_by_css_selector("span.txt1")

        count = int(len(user_info) / 4)
        print(count, end=".")

        for j in range(count):
            list_company.append(corp)
            list_code.append(stock_code)

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

        summary = driver.find_elements_by_css_selector("h2.us_label")

        for j in summary:
            list_summary.append(j.text)

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
    total_data["종목코드"] = pd.Series(list_code)
    total_data["날짜"] = pd.Series(list_date)
    total_data["직무"] = pd.Series(list_div)
    total_data["재직여부"] = pd.Series(list_cur)
    total_data["별점"] = pd.Series(list_stars)
    total_data["요약"] = pd.Series(list_summary)
    total_data["장점"] = pd.Series(list_merit)
    total_data["단점"] = pd.Series(list_disadvantages)
    total_data["경영진에게 바라는 점"] = pd.Series(list_managers)
    df = pd.concat([df, total_data])
    df.to_csv("Jobplanet_review.csv", encoding="utf-8", index=False)

    return df


def JP_rating(df, driver, corp, stock_code):
    try:
        try:
            star = driver.find_element_by_css_selector("span.rate_point")
        except:
            star = None
        stars = driver.find_elements(By.XPATH, '//*[@class="txt_point"]')
        try:
            복지급여 = float(stars[0].text)
        except:
            복지급여 = None
        try:
            워라밸 = float(stars[1].text)
        except:
            워라밸 = None
        try:
            사내문화 = float(stars[2].text)
        except:
            사내문화 = None
        try:
            승진가능성 = float(stars[3].text)
        except:
            승진가능성 = None
        try:
            경영진 = float(stars[4].text)
        except:
            경영진 = None

        pies = driver.find_elements(By.XPATH, '//*[@class="rate_pie_set"]')
        try:
            기업추천율 = float(re.sub(r"[^0-9]", "", pies[0].text)) / 100
        except:
            기업추천율 = None
        try:
            CEO지지율 = float(re.sub(r"[^0-9]", "", pies[1].text)) / 100
        except:
            CEO지지율 = None
        try:
            성장가능성 = float(re.sub(r"[^0-9]", "", pies[2].text)) / 100
        except:
            성장가능성 = None

        cnt = driver.find_element_by_css_selector("li.viewReviews").text.split("\n")[1]
        jp_dict = {
            "corp": corp,
            "stock_code": stock_code,
            "잡플래닛평점": float(star.text),
            "복지 및 급여": 복지급여,
            "업무와삶의균형": 워라밸,
            "사내문화": 사내문화,
            "승진기회및가능성": 승진가능성,
            "경영진": 경영진,
            "기업추천율": 기업추천율,
            "CEO지지율": CEO지지율,
            "성장가능성": 성장가능성,
            "잡플래닛개수": int(cnt),
        }
        df = pd.concat([df, pd.DataFrame([jp_dict])])
        df.to_csv("Jobplanet_rating.csv", encoding="utf-8", index=False)
    except:
        print(corp, "ERROR : NaN값 있음")
        pass
    return df


# email 본인 아이디, password 본인 패스워드 입력
# 리뷰를 남겨서 전체 접근이 가능한 상태여야 함
def JP_login(usr, pwd, driver):
    driver.get("https://www.jobplanet.co.kr/users/sign_in?_nav=gb")
    time.sleep(4)
    login_id = driver.find_element_by_css_selector("input#user_email")
    login_id.send_keys(usr)
    login_pwd = driver.find_element_by_css_selector("input#user_password")
    login_pwd.send_keys(pwd)
    login_id.send_keys(Keys.RETURN)
    time.sleep(4)
    return driver


def crawl_JP(usr, pwd, corp_list, mode):
    driver = webdriver.Chrome("chromedriver.exe")
    if mode == "JP_review":
        driver = JP_login(usr, pwd, driver)

    for i in range(len(corp_list)):
        corp = corp_list.iloc[i]["corp"]
        stock_code = corp_list.iloc[i]["stock_code"]

        try:
            search_query = driver.find_element_by_css_selector(
                "input#search_bar_search_query"
            )
            search_query.send_keys(corp)
            search_query.send_keys(Keys.RETURN)
            time.sleep(4)
            driver.find_element_by_css_selector("a.tit").click()
            time.sleep(4)
            try:
                driver.find_element_by_css_selector("li.viewReviews").click()
                time.sleep(4)
            except:
                pass
            try:
                driver.find_element_by_css_selector("button.btn_close_x_ty1 ").click()
                time.sleep(4)
            except:
                pass

            if mode == "JP_review":
                if i == 0:
                    df = pd.DataFrame()
                else:
                    df = pd.read_csv("Jobplanet_review.csv", encoding="utf-8")
                df = JP_review(df, driver, corp)

            elif mode == "JP_rating":
                if i == 0:
                    df = pd.DataFrame()
                else:
                    df = pd.read_csv("Jobplanet_rating.csv", encoding="utf-8")
                df = JP_rating(df, driver, corp, stock_code)

        except:
            print(corp, "ERROR : 검색 불가")
            driver.get("https://www.jobplanet.co.kr/job")
            time.sleep(4)
            pass
    driver.close()
    return df


def B_rating(df, driver, corp, stock_code):
    try:
        driver.get(f"https://www.teamblind.com/kr/company/{corp}/reviews?")
        time.sleep(5)
        try:
            if driver.find_element_by_css_selector("section.not-found"):
                print(corp, "NOT FOUND")
                driver.find_element_by_css_selector("button.btn-srch").click()
                time.sleep(5)
                search = driver.find_element_by_css_selector("input#keyword")
                search.send_keys(corp)
                search.send_keys(Keys.RETURN)
                time.sleep(5)
                driver.find_element(By.XPATH, '//*[@class="dtl"]/ul/li/a').click()
                time.sleep(5)
        except:
            pass
        stars = driver.find_elements(By.XPATH, '//*[@class="star"]')
        cnt = (
            driver.find_element_by_css_selector("em.count")
            .text.split()[0][:-1]
            .replace(",", "")
        )
        blind_dict = {
            "corp": corp,
            "stock_code": stock_code,
            "블라인드평점": float(stars[0].text.split("\n")[-1]),
            "블라인드개수": int(cnt),
            "커리어향상": float(stars[6].text),
            "업무와삶의균형": float(stars[7].text),
            "급여및복지": float(stars[8].text),
            "사내문화": float(stars[9].text),
            "경영진": float(stars[10].text),
        }
        df = pd.concat([df, pd.DataFrame([blind_dict])])
        df.to_csv("Blind_rating.csv", encoding="utf-8", index=False)
        print(corp, ": SUCCESS")
    except:
        print("*******", corp, "FAIL *******")
        pass
    return df


def B_review(df, driver, corp, stock_code):
    list_div = []
    list_cur = []
    list_date = []
    list_stars = []
    list_summary = []
    list_merit = []
    list_disadvantages = []

    for p in range(1, 16):
        try:
            print(p, "page")
            driver.get(f"https://www.teamblind.com/kr/company/{corp}/reviews?page={p}")
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
    total_data["회사"] = [corp] * len((list_date))
    total_data["종목코드"] = [stock_code] * len((list_date))
    total_data["날짜"] = pd.Series(list_date)
    total_data["직무"] = pd.Series(list_div)
    total_data["재직여부"] = pd.Series(list_cur)
    total_data["별점"] = pd.Series(list_stars)
    total_data["요약"] = pd.Series(list_summary)
    total_data["장점"] = pd.Series(list_merit)
    total_data["단점"] = pd.Series(list_disadvantages)
    df = pd.concat([df, total_data])
    df.to_csv("Blind_review.csv", encoding="utf-8", index=False)
    return df


def crawl_B(corp_list, mode):
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://www.teamblind.com/kr")
    if mode == "B_review":
        driver.find_element_by_css_selector("a.btn_signin").click()
        time.sleep(15)
    for i in range(len(corp_list)):
        corp = corp_list.iloc[i]["corp"]
        stock_code = corp_list.iloc[i]["stock_code"]
        if mode == "B_review":
            if i == 0:
                df = pd.DataFrame()
            else:
                df = pd.read_csv("Blind_review.csv", encoding="utf-8")
            df = B_review(df, driver, corp, stock_code)
        elif mode == "B_star":
            if i == 0:
                df = pd.DataFrame()
            else:
                df = pd.read_csv("Blind_rating.csv", encoding="utf-8")
            df = B_rating(df, driver, corp, stock_code)
    return df
