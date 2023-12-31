import pymysql
import pandas as pd
import numpy as np
import warnings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_utils import (
    save_data_to_csv,
    save_data_to_database,
)

warnings.filterwarnings("ignore", category=FutureWarning)


username = "root"
password = "****"
hostname = "localhost"
database_name = "Data_Mart"
desired_table_name = "credit_data_web"
DB_URL = f"mysql+pymysql://{username}:{password}@{hostname}/{database_name}"


cnx = pymysql.connect(
    user=username,
    password=password,
    host=hostname,
    database=database_name,
)

query = "SELECT * FROM Data_Warehouse.final_features;"
data = pd.read_sql(query, cnx)
cnx.close()

credit_data = data[["corp", "stock_code", "sector", "year"]].copy()

data.loc[:, "net_borrowings"] = data["borrowings"] - data["cash_and_equivalents"]
data.loc[:, "quick_assets"] = data["current_assets"] - data["inventory"]

# Metrics with * 100 for percentages
credit_data.loc[:, "ebitda_margin"] = data["ebitda"] / data["revenue"] * 100
credit_data.loc[:, "ebitda_to_interest_expense"] = (
    data["ebitda"] / data["interest"] * 100
)
credit_data.loc[:, "debt_ratio"] = (
    data["total_liabilities"] / data["total_equity"] * 100
)
credit_data.loc[:, "dependence_on_net_borrowings"] = (
    data["net_borrowings"] / data["total_assets"]
) * 100
credit_data.loc[:, "operating_cf_to_total_borrowings"] = (
    data["cash_flow_operating"] / data["borrowings"]
) * 100
credit_data.loc[:, "net_borrowings_to_ebitda"] = (
    data["net_borrowings"] / data["ebitda"] * 100
)
credit_data.loc[:, "revenue"] = data["revenue"]
credit_data.loc[:, "cogs"] = data["cost_of_sales"]
credit_data.loc[:, "selling_general_administrative_expenses"] = data[
    "selling_general_administrative_expenses"
]
credit_data.loc[:, "ebit"] = data["ebit"]
credit_data.loc[:, "ebit_margin"] = data["ebit"] / data["revenue"]
credit_data.loc[:, "ebitda_to_sales_revenue"] = data["ebitda"] / data["revenue"] * 100
credit_data.loc[:, "total_assets"] = data["total_assets"]
credit_data.loc[:, "return_on_assets"] = data["net_income"] / data["total_assets"] * 100
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
credit_data.loc[:, "borrowing_dependency"] = (
    data["borrowings"] / data["total_assets"] * 100
)
credit_data.loc[:, "total_borrowings_to_ebitda"] = (
    data["borrowings"] / data["ebitda"] * 100
)
credit_data.loc[:, "debt_to_net_income_ratio"] = (
    data["total_liabilities"] / data["net_income"]
) * 100
credit_data.loc[:, "total_assets_leverage"] = (
    data["total_assets"] / data["total_equity"]
) * 100
credit_data.loc[:, "current_liabilities"] = data["current_liabilities"]
credit_data.loc[:, "working_capital"] = (
    data["current_assets"] - data["current_liabilities"]
)
credit_data.loc[:, "current_liabilities_ratio"] = (
    data["current_liabilities"] / data["current_assets"]
) * 100
credit_data.loc[:, "quick_assets"] = data["quick_assets"]
credit_data.loc[:, "quick_ratio"] = (
    data["quick_assets"] / data["current_liabilities"] * 100
)
credit_data.loc[:, "cash_and_cash_equivalents"] = data["cash_and_equivalents"]
credit_data.loc[:, "short_term_borrowings"] = data["short_borrowing"]
credit_data.loc[:, "cash_and_cash_equivalents_to_short_term_borrowings_ratio"] = (
    data["cash_and_equivalents"] / data["short_borrowing"]
) * 100
credit_data.loc[:, "short_term_borrowings_to_total_borrowings_ratio"] = (
    data["short_borrowing"] / data["borrowings"]
) * 100
credit_data.loc[:, "days_sales_outstanding"] = (
    data["accounts_receivable"] / data["revenue"] * 365
)
credit_data.loc[:, "market_capitalization"] = data["market_capitalization"]


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
    "revenue": "매출액",
    "cogs": "매출원가",
    "selling_general_administrative_expenses": "판매관리비",
    "ebit": "EBIT",
    "ebit_margin": "EBIT마진",
    "ebitda_to_sales_revenue": "EBITDA/매출액",
    "total_assets": "자산총계",
    "return_on_assets": "총자산수익률()",
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
    "market_capitalization": "시가총액",
}

credit_data["label_ko"] = credit_data["label_en"].map(mapping)

cols = credit_data.columns.tolist()
cols.insert(cols.index("label_en") + 1, cols.pop(cols.index("label_ko")))
credit_data = credit_data[cols]

save_data_to_csv(credit_data, "credit_data_web.csv")

save_data_to_database(credit_data, "credit_data_web", DB_URL)
