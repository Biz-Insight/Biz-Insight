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
        "mysql+pymysql://{user}:{pw}@{host}/{db}?charset=utf8mb4".format(
            user=username, pw=password, db=database_name, host=hostname
        )
    )

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Change df name
        df.to_sql(desired_table_name, con=engine, if_exists="replace", index=False)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    # cursor.close()
    # cnx.close()


def insert_to_mysql(df, username, password, host_ip, database_name, desired_table_name):
    import pymysql
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    hostname = f"ec2-{host_ip}.ap-northeast-3.compute.amazonaws.com"

    cnx = pymysql.connect(user=username, password=password, host=hostname)
    cursor = cnx.cursor()

    engine = create_engine(
        "mysql+pymysql://{user}:{pw}@{host}/{db}?charset=utf8mb4".format(
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
        )
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    cursor.close()
    cnx.close()


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

    output_df.reset_index(drop=True)

    print("CRB index is crawled")

    return output_df
