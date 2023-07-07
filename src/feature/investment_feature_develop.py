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
desired_table_name = "investment_data"


cnx = pymysql.connect(
    user=username,
    password=password,
    host=hostname,
    database=database_name,
)

query = "SELECT * FROM dart_data.preprocessed;"
data = pd.read_sql(query, cnx)
cnx.close()

investment_data = data[["corp", "stock_code", "sector", "year"]].copy()

data["earnings_per_share"] = data["net_income"] / data["outstanding_shares"]
data["book_value_per_share"] = data["total_equity"] / data["outstanding_shares"]


# 수익성 (Profitability)
investment_data["gross_profit_margin"] = (data["gross_profit"] / data["revenue"]) * 100
investment_data["operating_profit_margin"] = (
    data["operating_income"] / data["revenue"]
) * 100
investment_data["net_profit_margin"] = (data["net_income"] / data["revenue"]) * 100
investment_data["ebitda_margin"] = (data["ebitda"] / data["revenue"]) * 100
investment_data["return_on_equity"] = (data["net_income"] / data["total_equity"]) * 100
investment_data["return_on_assets"] = (data["net_income"] / data["total_assets"]) * 100
investment_data["return_on_invested_capital"] = data["operating_income"] / (
    data["total_equity"] + data["total_liabilities"]
)

# 안정성 (Stability)
investment_data["debt_ratio"] = data["total_liabilities"] / data["total_assets"]
investment_data["current_ratio"] = data["current_assets"] / data["current_liabilities"]
investment_data["quick_ratio"] = (data["current_assets"] - data["inventory"]) / data[
    "current_liabilities"
]
investment_data["non_current_debt_ratio"] = (
    data["non_current_liabilities"] / data["total_assets"]
)
investment_data["equity_ratio"] = data["total_equity"] / data["total_assets"]
investment_data["interest_coverage_ratio"] = data["ebit"] / data["interest"]
investment_data["debt_to_equity_ratio"] = (
    data["total_liabilities"] / data["total_equity"]
)
investment_data["net_debt_ratio"] = (
    data["borrowings"] - data["cash_and_equivalents"]
) / data["total_assets"]
investment_data["retention_ratio"] = data["retained_earnings"] / data["net_income"]


# 가치지표 (Valuation Ratios)
investment_data["earnings_per_share"] = data["net_income"] / data["outstanding_shares"]
investment_data["book_value_per_share"] = (
    data["total_equity"] / data["outstanding_shares"]
)
investment_data["price_earnings_ratio"] = (
    data["stock_price"] / data["earnings_per_share"]
)
investment_data["price_to_book_ratio"] = (
    data["stock_price"] / data["book_value_per_share"]
)
investment_data["price_cash_flow_ratio"] = data["stock_price"] / (
    data["cash_flow_operating"] / data["outstanding_shares"]
)
investment_data["enterprise_value_to_ebitda"] = (
    data["stock_price"] * data["outstanding_shares"]
    + data["borrowings"]
    - data["cash_and_equivalents"]
) / data["ebitda"]


# 성장성 (Growth)
data_sorted = data.sort_values(["corp", "year"])

columns = [
    "revenue",
    "operating_income",
    "net_income",
    "total_assets",
    "fixed_assets",
    "total_liabilities",
    "total_equity",
]
growth_columns = [
    "revenue_growth_rate",
    "operating_income_growth_rate",
    "net_income_growth_rate",
    "total_asset_growth_rate",
    "fixed_asset_growth_rate",
    "total_liabilities_growth_rate",
    "total_equity_growth_rate",
]

for col, growth_col in zip(columns, growth_columns):
    data_sorted[growth_col] = data_sorted.groupby("corp")[col].pct_change() * 100
    data_sorted.loc[data_sorted.groupby("corp").head(1).index, growth_col] = np.nan

for growth_col in growth_columns:
    investment_data[growth_col] = data_sorted[growth_col]

# 활동성 (Efficiency)
investment_data["total_asset_turnover"] = data["revenue"] / data["total_assets"]
investment_data["return_on_equity"] = (data["net_income"] / data["total_equity"]) * 100
investment_data["net_working_capital_turnover"] = data["revenue"] / (
    data["current_assets"] - data["current_liabilities"]
)
investment_data["fixed_asset_turnover"] = data["revenue"] / data["fixed_assets"]
investment_data["accounts_receivable_turnover"] = (
    data["revenue"] / data["accounts_receivable"]
)
investment_data["inventory_turnover"] = data["cost_of_sales"] / data["inventory"]
investment_data["accounts_payable_turnover"] = (
    data["cost_of_sales"] / data["accounts_payable"]
)

id_vars = ["corp", "stock_code", "sector", "year"]
value_vars = investment_data.columns[4:]

melted_data = pd.melt(
    investment_data,
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

investment_data = pivot_table.copy()

investment_data = investment_data.replace([np.inf, -np.inf], np.nan)

mapping = {
    "gross_profit_margin": "매출총이익률",
    "operating_profit_margin": "영업이익률",
    "net_profit_margin": "순이익률",
    "ebitda_margin": "EBITDA마진율",
    "return_on_equity": "ROE",
    "return_on_assets": "ROA",
    "return_on_invested_capital": "ROIC",
    "debt_ratio": "부채비율",
    "current_ratio": "유동비율",
    "quick_ratio": "당좌비율",
    "non_current_debt_ratio": "비유동부채비율",
    "equity_ratio": "자기자본비율",
    "interest_coverage_ratio": "이자보상배율",
    "debt_to_equity_ratio": "차입금비율",
    "net_debt_ratio": "순부채비율",
    "retention_ratio": "자본유보율",
    "earnings_per_share": "EPS",
    "book_value_per_share": "BPS",
    "price_earnings_ratio": "PER",
    "price_to_book_ratio": "PBR",
    "price_cash_flow_ratio": "PCR",
    "enterprise_value_to_ebitda": "EV/EBITDA",
    "revenue_growth_rate": "매출액증가율",
    "operating_profit_growth_rate": "영업이익증가율",
    "net_income_growth_rate": "순이익증가율",
    "total_asset_growth_rate": "총자산증가율",
    "fixed_asset_growth_rate": "유형자산증가율",
    "total_debt_growth_rate": "부채총계증가율",
    "equity_growth_rate": "자기자본증가율",
    "total_asset_turnover": "총자산회전율",
    "net_working_capital_turnover": "순운전자본회전율",
    "fixed_asset_turnover": "유형자산회전율",
    "accounts_receivable_turnover": "매출채권회전율",
    "inventory_turnover": "재고자산회전율",
    "accounts_payable_turnover": "매입채무회전율",
}


investment_data["label_ko"] = investment_data["label_en"].map(mapping)

cols = investment_data.columns.tolist()
cols.insert(cols.index("label_en") + 1, cols.pop(cols.index("label_ko")))
investment_data = investment_data[cols]

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
    investment_data.to_sql(
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
