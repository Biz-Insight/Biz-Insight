import pymysql
import pandas as pd
import numpy as np
import warnings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

warnings.filterwarnings("ignore", category=FutureWarning)


username = "*****"
password = "*****"
hostname = "ec2-15-152-211-160.ap-northeast-3.compute.amazonaws.com"
database_name = "dart_data"
desired_table_name = "credit_data"


cnx = pymysql.connect(
    user=username,
    password=password,
    host=hostname,
    database=database_name,
)

query = "SELECT * FROM dart_data.preprocessed;"
data = pd.read_sql(query, cnx)
cnx.close()

credit_data = data[["corp", "stock_code", "sector", "year"]].copy()

data.loc[:, "net_borrowings"] = data["borrowings"] - data["cash_and_equivalents"]
data.loc[:, "quick_assets"] = data["current_assets"] - data["inventory"]

credit_data.loc[:, "ebitda_margin"] = data["ebitda"] / data["revenue"] * 100
credit_data.loc[:, "ebitda_to_interest_expense"] = data["ebitda"] / data["interest"]
credit_data.loc[:, "debt_ratio"] = data["total_liabilities"] / data["total_assets"]
credit_data.loc[:, "dependence_on_net_borrowings"] = (
    data["borrowings"] / data["total_equity"]
)
credit_data.loc[:, "operating_cf_to_total_borrowings"] = (
    data["cash_flow_operating"] / data["borrowings"]
)
credit_data.loc[:, "net_borrowings_to_ebitda"] = data["net_borrowings"] / data["ebitda"]
credit_data.loc[:, "sales_revenue"] = data["revenue"]
credit_data.loc[:, "cogs"] = data["cost_of_sales"]
credit_data.loc[:, "selling_general_administrative_expenses"] = data[
    "selling_general_administrative_expenses"
]
credit_data.loc[:, "ebit"] = data["ebit"]
credit_data.loc[:, "ebit_margin"] = data["ebit"] / data["revenue"] * 100
credit_data.loc[:, "ebitda_to_sales_revenue"] = data["ebitda"] / data["revenue"]
credit_data.loc[:, "total_assets"] = data["total_assets"]
credit_data.loc[:, "roa"] = data["net_income"] / data["total_assets"] * 100
credit_data.loc[:, "ebitda"] = data["ebitda"]
credit_data.loc[:, "financial_expenses"] = data["interest"]
credit_data.loc[:, "corporate_tax"] = data["tax"]
credit_data.loc[:, "operating_cash_flow"] = data["cash_flow_operating"]
credit_data.loc[:, "free_cash_flow"] = (
    data["cash_flow_operating"] - data["cash_flow_investing"]
)
credit_data.loc[:, "total_liabilities"] = data["total_liabilities"]
credit_data.loc[:, "total_equity"] = data["total_equity"]
credit_data.loc[:, "total_borrowings"] = data["borrowings"]
credit_data.loc[:, "net_borrowings"] = data["net_borrowings"]
credit_data.loc[:, "borrowing_dependency"] = data["borrowings"] / data["total_equity"]
credit_data.loc[:, "total_borrowings_to_ebitda"] = data["borrowings"] / data["ebitda"]
credit_data.loc[:, "debt_to_net_income_ratio"] = (
    data["total_liabilities"] / data["net_income"]
)
credit_data.loc[:, "total_assets_leverage"] = (
    data["total_assets"] / data["total_equity"]
)
credit_data.loc[:, "current_liabilities"] = data["current_liabilities"]
credit_data.loc[:, "working_capital"] = (
    data["current_assets"] - data["current_liabilities"]
)
credit_data.loc[:, "current_liabilities_ratio"] = (
    data["current_liabilities"] / data["current_assets"]
)
credit_data.loc[:, "quick_assets"] = data["quick_assets"]
credit_data.loc[:, "quick_ratio"] = data["quick_assets"] / data["current_liabilities"]
credit_data.loc[:, "cash_and_cash_equivalents"] = data["cash_and_equivalents"]
credit_data.loc[:, "short_term_borrowings"] = data["short_borrowing"]
credit_data.loc[:, "cash_and_cash_equivalents_to_short_term_borrowings_ratio"] = (
    data["cash_and_equivalents"] / data["short_borrowing"]
)
credit_data.loc[:, "short_term_borrowings_to_total_borrowings_ratio"] = (
    data["short_borrowing"] / data["borrowings"]
)
credit_data.loc[:, "days_sales_outstanding"] = (
    data["accounts_receivable"] / data["revenue"] * 365
)
credit_data.loc[:, "average_accounts_receivable_per_sales_turnover"] = (
    data["accounts_receivable"] / data["revenue"]
)


id_vars = ["corp", "stock_code", "sector", "year"]
value_vars = credit_data.columns[4:]

melted_data = pd.melt(
    credit_data,
    id_vars=id_vars,
    value_vars=value_vars,
    var_name="label_en",
    value_name="value",
)
pivot_table = pd.pivot_table(
    melted_data,
    index=["corp", "stock_code", "sector", "label_en"],
    columns="year",
    values="value",
)
pivot_table.reset_index(inplace=True)
pivot_table["YoY"] = (
    (pivot_table["2022"] - pivot_table["2021"]) / pivot_table["2021"] * 100
)

credit_data = pivot_table.copy()

credit_data = credit_data.replace([np.inf, -np.inf], np.nan)

mapping = {
    "ebitda_margin": "EBITDA마진",
    "ebitda_to_interest_expense": "EBITDA/금융비용",
    "debt_ratio": "부채비율",
    "dependence_on_net_borrowings": "순차입금의존도",
    "operating_cf_to_total_borrowings": "영업현금흐름/총차입금",
    "net_borrowings_to_ebitda": "순차입금/EBITDA",
    "sales_revenue": "매출액",
    "cogs": "매출원가",
    "selling_general_administrative_expenses": "판매관리비",
    "ebit": "EBIT",
    "ebit_margin": "EBIT마진",
    "ebitda_to_sales_revenue": "EBITDA/매출액",
    "total_assets": "자산총계",
    "roa": "총자산수익률(ROA)",
    "ebitda": "EBITDA",
    "financial_expenses": "금융비용",
    "corporate_tax": "법인세납부",
    "operating_cash_flow": "영업활동현금흐름",
    "free_cash_flow": "잉여현금흐름",
    "total_liabilities": "부채총계",
    "total_equity": "자본총계",
    "total_borrowings": "총차입금",
    "net_borrowings": "순차입금",
    "borrowing_dependency": "차입금의존도",
    "total_borrowings_to_ebitda": "총차입금/EBITDA",
    "debt_to_net_income_ratio": "총부채상환비율",
    "total_assets_leverage": "총자산레버리지",
    "current_liabilities": "유동부채금액",
    "working_capital": "운전자본",
    "current_liabilities_ratio": "유동부채비율",
    "quick_assets": "당좌자산",
    "quick_ratio": "당좌비율",
    "cash_and_cash_equivalents": "현금성자산",
    "short_term_borrowings": "단기성차입금",
    "cash_and_cash_equivalents_to_short_term_borrowings_ratio": "현금성자산/단기성차입금",
    "short_term_borrowings_to_total_borrowings_ratio": "단기성차입금/총차입금",
    "days_sales_outstanding": "매출채권회전일수",
    "average_accounts_receivable_per_sales_turnover": "1회당회전매출채권액수",
}

credit_data["label_ko"] = credit_data["label_en"].map(mapping)

cols = credit_data.columns.tolist()
cols.insert(cols.index("label_en") + 1, cols.pop(cols.index("label_ko")))
credit_data = credit_data[cols]

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
    credit_data.to_sql(
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
