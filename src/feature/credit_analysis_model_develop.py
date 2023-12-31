import pymysql
import pandas as pd
import warnings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_utils import (
    save_data_to_csv,
    save_data_to_database,
)


warnings.filterwarnings("ignore", category=FutureWarning)


def get_database_connection():
    return pymysql.connect(
        user=username, password=password, host=hostname, database=database_name
    )


def fetch_data(query):
    with get_database_connection() as conn:
        return pd.read_sql(query, conn)


def process_model(model, model_filter):
    model_processed = model.copy()

    indices_to_drop = set()

    for col in model_filter:
        sorted_col = model_processed[col].sort_values()

        top3_indices = sorted_col[-3:].index.tolist()
        bottom3_indices = (
            sorted_col[:3].index.tolist() if sorted_col[:3].min() < 0 else []
        )

        for idx in top3_indices + bottom3_indices:
            indices_to_drop.add(idx)

    model_processed = model_processed.drop(indices_to_drop)
    model_processed.reset_index(drop=True, inplace=True)

    return model_processed


username = "root"
password = "****"
hostname = "localhost"
database_name = "Data_Mart"
DB_URL = f"mysql+pymysql://{username}:{password}@{hostname}/{database_name}"

cnx = get_database_connection()

credit_data = fetch_data("SELECT * FROM Data_Warehouse.credit_data_model")
economic_indicators = fetch_data("SELECT * FROM Data_Warehouse.economic_indicators")
credit_rank = fetch_data("SELECT * FROM Data_Warehouse.credit_rank")
rating_filled = fetch_data("SELECT * FROM Data_Warehouse.rating_filled")
crb_index = fetch_data("SELECT * FROM Data_Lake.crb_index")
investment_data = fetch_data("SELECT * FROM Data_Warehouse.investment_data_model")

cnx.close()

avg_crb_index = crb_index.copy().groupby("year")["crb_index"].mean().reset_index()
avg_crb_index.columns = ["year", "crb_index_avg"]
avg_crb_index["year"] = avg_crb_index["year"].astype(int).astype(str)

credit_analysis_features = credit_data.merge(economic_indicators, how="left", on="year")

credit_rank_subset = credit_rank[["corp", "year", "rank"]]
credit_analysis_features = credit_analysis_features.copy().merge(
    credit_rank_subset, how="left", on=["corp", "year"]
)

rating_filled_subset = rating_filled.drop(["stock_code", "sector"], axis=1)
credit_analysis_features = credit_analysis_features.copy().merge(
    rating_filled_subset, how="left", on="corp"
)

credit_analysis_features = credit_analysis_features.merge(
    avg_crb_index, how="left", on="year"
)

credit_analysis_model_a = credit_analysis_features.copy()

current_features = set(credit_analysis_features.columns)
investment_features = set(investment_data.columns)
common_features = list(investment_features & current_features)

common_features.remove("corp")
common_features.remove("year")
common_features.remove("sector")
common_features.remove("stock_code")

investment_data = investment_data.drop(common_features, axis=1)

credit_analysis_features = credit_analysis_features.merge(
    investment_data, how="left", on=["corp", "year", "stock_code", "sector"]
)

credit_analysis_model_b = credit_analysis_features.copy()

for model in [credit_analysis_model_a, credit_analysis_model_b]:
    model.rename(
        columns={
            "minimum_wag": "minimum_wage",
            "uskor_exchange_average": "us_kor_exchange_avg",
            "PPI_year": "ppi_year",
        },
        inplace=True,
    )


model_a_filter = [
    "ebitda_margin",
    "ebitda_to_interest_expense",
    "debt_ratio",
    "dependence_on_net_borrowings",
    "net_borrowings_to_ebitda",
    "ebit_margin",
    "ebitda_to_sales_revenue",
    "borrowing_dependency",
    "total_borrowings_to_ebitda",
    "debt_to_net_income_ratio",
    "total_assets_leverage",
    "current_liabilities_ratio",
    "quick_ratio",
    "days_sales_outstanding",
]

investment_data_filter = [
    "return_on_equity",
    "return_on_invested_capital",
    "current_ratio",
    "non_current_debt_ratio",
    "equity_ratio",
    "interest_coverage_ratio",
    "debt_to_equity_ratio",
    "retention_ratio",
    "earnings_per_share",
    "book_value_per_share",
    "price_earnings_ratio",
    "price_to_book_ratio",
    "price_cash_flow_ratio",
    "enterprise_value_to_ebitda",
    "net_working_capital_turnover",
    "tangible_asset_turnover",
    "accounts_receivable_turnover",
    "inventory_turnover",
    "accounts_payable_turnover",
]

model_b_filter = model_a_filter + investment_data_filter

credit_model_a = process_model(credit_analysis_model_a, model_a_filter)
credit_model_b = process_model(credit_analysis_model_b, model_b_filter)

save_data_to_csv(credit_model_a, "credit_model_a.csv")
save_data_to_csv(credit_model_b, "credit_model_b.csv")

save_data_to_database(credit_model_a, "credit_model_a", DB_URL)
save_data_to_database(credit_model_b, "credit_model_b", DB_URL)
