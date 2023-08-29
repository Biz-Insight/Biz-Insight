import warnings
import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

warnings.filterwarnings("ignore", category=FutureWarning)

username = "root"
password = "****"
hostname = "localhost"
database_name = "Data_Mart"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{hostname}/{database_name}"
)

query = "SELECT * FROM Data_Mart.industry_average_year;"
industry_average = pd.read_sql(query, engine)

query = "SELECT * FROM Data_Lake.crb_index;"
crb_index = pd.read_sql(query, engine)

query = "SELECT * FROM Data_Warehouse.economic_indicators;"
economic_indicators = pd.read_sql(query, engine)

query = "SELECT * FROM Data_Mart.credit_model_a;"
model_a = pd.read_sql(query, engine)


rank_mapping = {
    "AAA": 9,
    "AA+": 8,
    "AA": 7,
    "AA-": 6,
    "A+": 5,
    "A": 4,
    "A-": 3,
    "BBB": 2,
    "JB": 1,
}

# Comment out this section if need to train model and save it to .pkl
###############################################################################
model_with_y = (
    model_a[model_a["rank"].notna()]
    .reset_index(drop=True)
    .drop(["corp", "stock_code", "sector", "year"], axis=1)
)
model_without_y = (
    model_a[model_a["rank"].isna()].reset_index(drop=True).drop(["rank"], axis=1)
)

# 선정한 모델
X = model_with_y.drop("rank", axis=1)
y = model_with_y["rank"]
y = y.map(rank_mapping)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# clf = RandomForestClassifier(
#     criterion="entropy",
#     max_depth=18,
#     max_features="sqrt",
#     n_estimators=500,
#     random_state=42,
# )
# clf.fit(X_train, y_train)
###############################################################################
with open("rf_model.pkl", "rb") as file:
    clf = pickle.load(file)


# y_pred = clf.predict(X_test)

# 엑셀에서 데이터프레임으로 읽어오기
fs = pd.read_excel("Credit_Prediction.xlsx", sheet_name=None)
corp_info = fs["corp_info"]
bs = fs["bs"]
incs = fs["incs"]
cf = fs["cf"]

# 액셀에서 계정 값 받아오기
sector = corp_info["산업"][0]
revenue = incs["계정값"][0]
cost_of_sales = incs["계정값"][1]
gross_profit = incs["계정값"][2]
operating_income = incs["계정값"][6]
net_income = incs["계정값"][11]
ebit = incs["계정값"][9]
depreciation_amortization = incs["계정값"][5]
ebitda = ebit + depreciation_amortization
total_equity = bs["계정값"][34]
total_assets = bs["계정값"][14]
total_liabilities = bs["계정값"][26]
current_assets = bs["계정값"][1]
current_liabilities = bs["계정값"][16]
non_current_liabilities = bs["계정값"][21]
short_borrowing = bs["계정값"][19]
long_borrowing = bs["계정값"][22]
cash_and_equivalents = bs["계정값"][2]
retained_earnings = bs["계정값"][30]
tangible_assets = bs["계정값"][11]
intangible_assets = bs["계정값"][12]
accounts_receivable = bs["계정값"][4]
inventory = bs["계정값"][5]
accounts_payable = bs["계정값"][17]
outstanding_shares = corp_info["발행주식수"][0]
cash_flow_operating = cf["계정값"][0]
selling_general_administrative_expenses = incs["계정값"][4]
cash_flow_investing = cf["계정값"][8]
cash_flow_financing = cf["계정값"][12]
long_term_assets = bs["계정값"][8]
interest = incs["계정값"][7]
tax = incs["계정값"][10]
stock_price = corp_info["현재주가"][0]
market_capitalization = stock_price * outstanding_shares
borrowings = short_borrowing + long_borrowing
net_liabilities = total_liabilities - total_assets
fixed_assets = bs["계정값"][9]
cash_flow_per_share = cash_flow_operating / outstanding_shares

# 신용지표 피쳐
net_borrowings = borrowings - cash_and_equivalents
quick_assets = current_assets - inventory

ebitda_margin = ebitda / revenue * 100
ebitda_to_interest_expense = ebitda / interest
debt_ratio = total_liabilities / total_assets
dependence_on_net_borrowings = borrowings / total_equity
net_borrowings_to_ebitda = net_borrowings / ebitda
cogs = cost_of_sales
selling_general_administrative_expenses = selling_general_administrative_expenses
ebit = ebit
ebit_margin = ebit / revenue * 100
ebitda_to_sales_revenue = ebitda / revenue
total_assets = total_assets
return_on_assets = net_income / total_assets * 100
financial_expenses = interest
corporate_tax = tax
operating_cash_flow = cash_flow_operating
free_cash_flow = cash_flow_operating - cash_flow_investing
total_liabilities = total_liabilities
total_equity = total_equity
total_borrowings = borrowings
net_borrowings = net_borrowings
borrowing_dependency = borrowings / total_equity
total_borrowings_to_ebitda = borrowings / ebitda
debt_to_net_income_ratio = total_liabilities / net_income
total_assets_leverage = total_assets / total_equity
current_liabilities = current_liabilities
working_capital = current_assets - current_liabilities
current_liabilities_ratio = current_liabilities / current_assets
quick_assets = quick_assets
quick_ratio = quick_assets / current_liabilities
cash_and_cash_equivalents = cash_and_equivalents
short_term_borrowings = short_borrowing
days_sales_outstanding = accounts_receivable / revenue * 365
market_capitalization = market_capitalization

# 질적데이터 피쳐
minimum_wage = model_a[model_a["year"] == "2022"]["minimum_wage"].values[0]
us_kor_exchange_avg = model_a[model_a["year"] == "2022"]["us_kor_exchange_avg"].values[
    0
]
ppi_year = model_a[model_a["year"] == "2022"]["ppi_year"].values[0]
kor_usa_ir_diff = model_a[model_a["year"] == "2022"]["kor_usa_ir_diff"].values[0]
kr_standard_yield = model_a[model_a["year"] == "2022"]["kr_standard_yield"].values[0]
crb_index_avg = crb_index[crb_index["year"] == 2023]["crb_index"].mean()

# 리뷰데이터 피쳐
count = industry_average[industry_average["sector"] == sector]["count"].values[0]
rating = industry_average[industry_average["sector"] == sector]["rating"].values[0]
paywellfare = industry_average[industry_average["sector"] == sector][
    "paywellfare"
].values[0]
worklifebal = industry_average[industry_average["sector"] == sector][
    "worklifebal"
].values[0]
culture = industry_average[industry_average["sector"] == sector]["culture"].values[0]
opportunity = industry_average[industry_average["sector"] == sector][
    "opportunity"
].values[0]
manager = industry_average[industry_average["sector"] == sector]["manager"].values[0]
recommend = industry_average[industry_average["sector"] == sector]["recommend"].values[
    0
]
ceo = industry_average[industry_average["sector"] == sector]["ceo"].values[0]
potential = industry_average[industry_average["sector"] == sector]["potential"].values[
    0
]

# 투자지표 피쳐
# earnings_per_share = net_income / outstanding_shares
# book_계정값_per_share = total_equity / outstanding_shares

# gross_profit_margin = gross_profit / revenue * 100
# operating_profit_margin = operating_income / revenue * 100
# net_profit_margin = net_income / revenue * 100
# ebitda_margin = ebitda / revenue * 100
# return_on_equity = net_income / total_equity * 100
# return_on_assets = net_income / total_assets * 100
# return_on_invested_capital = operating_income / (total_equity + total_liabilities)

# debt_ratio = total_liabilities / total_assets
# current_ratio = current_assets / current_liabilities
# quick_ratio = (current_assets - inventory) / current_liabilities
# non_current_debt_ratio = non_current_liabilities / total_assets
# equity_ratio = total_equity / total_assets
# interest_coverage_ratio = ebit / interest
# debt_to_equity_ratio = total_liabilities / total_equity
# net_debt_ratio = (borrowings - cash_and_equivalents) / total_assets
# retention_ratio = retained_earnings / net_income

# earnings_per_share = net_income / outstanding_shares
# book_계정값_per_share = total_equity / outstanding_shares
# price_earnings_ratio = stock_price / earnings_per_share
# price_to_book_ratio = stock_price / book_계정값_per_share
# price_cash_flow_ratio = stock_price / (cash_flow_operating / outstanding_shares)
# enterprise_계정값_to_ebitda = (
#     market_capitalization + borrowings - cash_and_equivalents
# ) / ebitda

# market_capitalization = market_capitalization

# total_asset_turnover = revenue / total_assets
# return_on_equity = net_income / total_equity * 100
# net_working_capital_turnover = revenue / (current_assets - current_liabilities)
# fixed_asset_turnover = revenue / fixed_assets
# accounts_receivable_turnover = revenue / accounts_receivable
# inventory_turnover = cost_of_sales / inventory
# accounts_payable_turnover = cost_of_sales / accounts_payable

# 예측을 위한 데이터 데이터프레임으로 변경
predict_data = pd.DataFrame(
    {
        "ebitda_margin": [ebitda_margin],
        "ebitda_to_interest_expense": [ebitda_to_interest_expense],
        "debt_ratio": [debt_ratio],
        "dependence_on_net_borrowings": [dependence_on_net_borrowings],
        "net_borrowings_to_ebitda": [net_borrowings_to_ebitda],
        "revenue": [revenue],
        "cogs": [cogs],
        "selling_general_administrative_expenses": [
            selling_general_administrative_expenses
        ],
        "ebit": [ebit],
        "ebit_margin": [ebit_margin],
        "ebitda_to_sales_revenue": [ebitda_to_sales_revenue],
        "total_assets": [total_assets],
        "return_on_assets": [return_on_assets],
        "ebitda": [ebitda],
        "financial_expenses": [financial_expenses],
        "corporate_tax": [corporate_tax],
        "operating_cash_flow": [operating_cash_flow],
        "free_cash_flow": [free_cash_flow],
        "total_liabilities": [total_liabilities],
        "total_equity": [total_equity],
        "total_borrowings": [total_borrowings],
        "net_borrowings": [net_borrowings],
        "borrowing_dependency": [borrowing_dependency],
        "total_borrowings_to_ebitda": [total_borrowings_to_ebitda],
        "debt_to_net_income_ratio": [debt_to_net_income_ratio],
        "total_assets_leverage": [total_assets_leverage],
        "current_liabilities": [current_liabilities],
        "working_capital": [working_capital],
        "current_liabilities_ratio": [current_liabilities_ratio],
        "quick_assets": [quick_assets],
        "quick_ratio": [quick_ratio],
        "cash_and_cash_equivalents": [cash_and_cash_equivalents],
        "short_term_borrowings": [short_term_borrowings],
        "days_sales_outstanding": [days_sales_outstanding],
        "market_capitalization": [market_capitalization],
        "minimum_wage": [minimum_wage],
        "us_kor_exchange_avg": [us_kor_exchange_avg],
        "ppi_year": [ppi_year],
        "kor_usa_ir_diff": [kor_usa_ir_diff],
        "kr_standard_yield": [kr_standard_yield],
        "count": [count],
        "rating": [rating],
        "paywellfare": [paywellfare],
        "worklifebal": [worklifebal],
        "culture": [culture],
        "opportunity": [opportunity],
        "manager": [manager],
        "recommend": [recommend],
        "ceo": [ceo],
        "potential": [potential],
        "crb_index_avg": [crb_index_avg],
        # "gross_profit_margin": [gross_profit_margin],
        # "operating_profit_margin": [operating_profit_margin],
        # "net_profit_margin": [net_profit_margin],
        # "return_on_equity": [return_on_equity],
        # "return_on_invested_capital": [return_on_invested_capital],
        # "current_ratio": [current_ratio],
        # "non_current_debt_ratio": [non_current_debt_ratio],
        # "equity_ratio": [equity_ratio],
        # "interest_coverage_ratio": [interest_coverage_ratio],
        # "debt_to_equity_ratio": [debt_to_equity_ratio],
        # "net_debt_ratio": [net_debt_ratio],
        # "retention_ratio": [retention_ratio],
        # "earnings_per_share": [earnings_per_share],
        # "book_계정값_per_share": [book_계정값_per_share],
        # "price_earnings_ratio": [price_earnings_ratio],
        # "price_to_book_ratio": [price_to_book_ratio],
        # "price_cash_flow_ratio": [price_cash_flow_ratio],
        # "enterprise_계정값_to_ebitda": [enterprise_계정값_to_ebitda],
        # "operating_income": [operating_income],
        # "net_income": [net_income],
        # "fixed_assets": [fixed_assets],
        # "total_asset_turnover": [total_asset_turnover],
        # "net_working_capital_turnover": [net_working_capital_turnover],
        # "fixed_asset_turnover": [fixed_asset_turnover],
        # "accounts_receivable_turnover": [accounts_receivable_turnover],
        # "inventory_turnover": [inventory_turnover],
        # "accounts_payable_turnover": [accounts_payable_turnover],
    }
)

rank_prediction = clf.predict(predict_data)
rank_mapping_reverse = {v: k for k, v in rank_mapping.items()}
prediction = rank_mapping_reverse[rank_prediction[0]]

print(f"신용등급 예측결과: '{prediction}'")
