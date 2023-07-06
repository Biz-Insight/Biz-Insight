def import_from_mysql(username, password, host_ip, database_name, desired_table_name):
    import pymysql
    import pandas as pd
    from sqlalchemy import create_engine

    hostname = f"ec2-{host_ip}.ap-northeast-3.compute.amazonaws.com"

    connection_str = f"mysql+pymysql://{username}:{password}@{hostname}/{database_name}"
    engine = create_engine(connection_str)
    query = f"SELECT * FROM {desired_table_name}"

    return pd.read_sql(query, engine)


def export_to_mysql(df, username, password, host_ip, database_name, desired_table_name):
    import pymysql
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    hostname = f"ec2-{host_ip}.ap-northeast-3.compute.amazonaws.com"

    cnx = pymysql.connect(user=username, password=password, host=hostname)
    cursor = cnx.cursor()

    engine = create_engine(
        "mysql+pymysql://{user}:{pw}@{host}/{db}?charset=utf8".format(
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
            dtype={"corp": "VARCHAR(255)"},
        )
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    cursor.close()
    cnx.close()


def insert_to_mysql(df, username, password, host_ip, database_name, desired_table_name):
    import pymysql
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    hostname = f"ec2-{host_ip}.ap-northeast-3.compute.amazonaws.com"

    cnx = pymysql.connect(user=username, password=password, host=hostname)
    cursor = cnx.cursor()

    engine = create_engine(
        "mysql+pymysql://{user}:{pw}@{host}/{db}?charset=utf8".format(
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
            if_exists="append",
            index=False,
            chunksize=1000,
            dtype={"corp": "VARCHAR(255)"},
        )
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    cursor.close()
    cnx.close()


def crawl_realtime_data(df, today):
    import urllib.request
    import pandas as pd
    import json

    corp_list = df.values.tolist()

    realtime_list = []

    for corp_set in corp_list:
        item_name = corp_set[0]
        item_code = corp_set[1]
        url = f"https://api.finance.naver.com/service/itemSummary.nhn?itemcode={item_code}"

        raw_data = urllib.request.urlopen(url).read()
        json_data = json.loads(raw_data)

        ######################################
        crawl_dict = {}

        crawl_dict["corp"] = item_name
        crawl_dict["stock_code"] = item_code
        crawl_dict["date"] = today
        crawl_dict["marketSum"] = json_data["marketSum"]
        crawl_dict["per"] = json_data["per"]
        crawl_dict["eps"] = json_data["eps"]
        crawl_dict["pbr"] = json_data["pbr"]
        crawl_dict["now"] = json_data["now"]
        ######################################

        print(f"{today} : {item_name}, done.")

        realtime_list.append(crawl_dict)

    return pd.DataFrame(realtime_list)


def crawl_stock_price(df, start_time, end_time, time_frame):
    from urllib import parse
    from ast import literal_eval
    import requests
    import pandas as pd

    corp_list = df.values.tolist()

    corp_stock_price_df = pd.DataFrame(
        columns=["날짜", "시가", "고가", "저가", "종가", "거래량", "외국인소진율", "stock_code", "corp"]
    )

    for corp_num in corp_list:
        item_name = corp_num[0]
        item_code = corp_num[1]

        get_param = {
            "symbol": item_code,
            "requestType": 1,
            "startTime": start_time,
            "endTime": end_time,
            "timeframe": time_frame,
        }

        get_param = parse.urlencode(get_param)
        url = "https://api.finance.naver.com/siseJson.naver?%s" % get_param
        response = requests.get(url)

        stock_df = pd.DataFrame(
            data=literal_eval(response.text.strip())[1:],
            columns=literal_eval(response.text.strip())[0],
        )

        stock_df["stock_code"] = corp_num[1]
        stock_df["corp"] = corp_num[0]

        corp_stock_price_df = pd.concat([corp_stock_price_df, stock_df], axis=0)

        print(item_name + "is done.")

    corp_stock_price_df = corp_stock_price_df[
        ["corp", "stock_code", "날짜", "시가", "고가", "저가", "종가", "거래량", "외국인소진율"]
    ]

    output_df = corp_stock_price_df.rename(
        columns={
            "날짜": "date",
            "시가": "open",
            "고가": "high",
            "저가": "low",
            "종가": "close",
            "거래량": "amount",
            "외국인소진율": "foreign_ownership_ratio",
        }
    )

    output_df["date"] = pd.to_datetime(output_df["date"], format="%Y%m%d").dt.strftime(
        "%Y-%m-%d"
    )

    output_df = output_df.applymap(lambda x: x.decode("utf-8"))

    output_df.reset_index(drop=True)

    return output_df


def crawl_crb_data(from_year):
    from datetime import date
    import pandas as pd
    from urllib.request import urlopen, Request
    import requests
    import json

    this_year = int(date.today().strftime("%Y"))
    year = this_year - from_year

    url = f"https://markets.tradingeconomics.com/chart?s=crytr:ind&interval=1d&span={year}y&securify=new&url=/commodity/crb&AUTH=4TzQudd9C53MSIZTEwrrMXxG1kRn%2FtcsPGnN1ASh%2Bien98aolBk0GUseDlaKinXh&ohlc=0"

    req = Request(url)
    html_text = urlopen(req).read()
    data_str = html_text.decode("utf-8")

    parsed_data = json.loads(data_str)["series"][0]["data"]
    parsed_df = pd.DataFrame(parsed_data)

    crb_df = parsed_df[["date", "y"]].copy()
    crb_df.rename(columns={"y": "crb_index"}, inplace=True)

    crb_df["date"] = crb_df["date"].str.split("T").str[0]

    for date, i in [("year", 0), ("month", 1), ("day", 2)]:
        crb_df[date] = crb_df["date"].str.split("-").str[i]

    crb_df.drop("date", axis=1, inplace=True)
    output_df = crb_df[["year", "month", "day", "crb_index"]]

    output_df = output_df.applymap(lambda x: x.decode("utf-8"))

    output_df.reset_index(drop=True)

    print("CRB index is crawled")

    return output_df
