import pymysql
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

username = "multi"
password = "Campus123!"
hostname = "ec2-15-152-211-160.ap-northeast-3.compute.amazonaws.com"
database_name = "Data_Mart"
desired_table_name = "main_fs"


def reshape_and_append(preprocessed_tmp, column_name, fs_type, label_ko, main_fs):
    data = preprocessed_tmp[["corp", "stock_code", "sector", "year", column_name]]

    reshaped_data = data.pivot_table(
        index=["corp", "stock_code", "sector"], columns="year", values=column_name
    ).reset_index()

    reshaped_data.columns = [
        str(col) if isinstance(col, int) else col for col in reshaped_data.columns
    ]

    reshaped_data["fs_type"] = fs_type
    reshaped_data["label_en"] = column_name
    reshaped_data["label_ko"] = label_ko

    reshaped_data["YoY"] = reshaped_data.apply(
        lambda row: np.nan
        if row["2021"] == 0
        else round(((row["2022"] - row["2021"]) / row["2021"]) * 100, 1),
        axis=1,
    )

    reshaped_data = reshaped_data[
        [
            "fs_type",
            "corp",
            "stock_code",
            "sector",
            "label_en",
            "label_ko",
            "2018",
            "2019",
            "2020",
            "2021",
            "2022",
            "YoY",
        ]
    ]

    return pd.concat([main_fs, reshaped_data], ignore_index=True)


cnx = pymysql.connect(
    user=username,
    password=password,
    host=hostname,
    database=database_name,
)

query = "SELECT * FROM Data_Warehouse.final_features;"
preprocessed_tmp = pd.read_sql(query, cnx)
cnx.close()

main_fs_info_list = [
    ["total_assets", "bs", "자산총계"],
    ["tangible_assets", "bs", "유형자산"],
    ["intangible_assets", "bs", "무형자산"],
    ["cash_and_equivalents", "bs", "현금및현금성자산"],
    ["total_equity", "bs", "자본총계"],
    ["total_liabilities", "bs", "부채총계"],
    ["revenue", "incs", "매출액"],
    ["cost_of_sales", "incs", "매출원가"],
    ["selling_general_administrative_expenses", "incs", "판매비와관리비"],
    ["operating_income", "incs", "영업이익"],
    ["net_income", "incs", "당기순이익"],
    ["cash_flow_operating", "cf", "영업활동현금흐름"],
    ["cash_flow_investing", "cf", "투자활동현금흐름"],
    ["cash_flow_financing", "cf", "재무활동현금흐름"],
]

main_fs = pd.DataFrame()

for info in main_fs_info_list:
    column_name, fs_type, label_ko = info
    main_fs = reshape_and_append(
        preprocessed_tmp=preprocessed_tmp,
        column_name=column_name,
        fs_type=fs_type,
        label_ko=label_ko,
        main_fs=main_fs,
    )

main_fs.to_csv("main_fs.csv", encoding="utf-8-sig", index=False)

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
    main_fs.to_sql(
        desired_table_name, con=engine, if_exists="replace", index=False, chunksize=1000
    )
    session.commit()
except:
    session.rollback()
    raise
finally:
    session.close()

cursor.close()
cnx.close()
