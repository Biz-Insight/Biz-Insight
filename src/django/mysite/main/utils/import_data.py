from .settings1 import *
from django.conf import settings


# reviews data
def import_from_mysql(username, password, host_ip, database_name, desired_table_name):
    import pymysql
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    hostname = f"ec2-{host_ip}.ap-northeast-3.compute.amazonaws.com"

    connection_str = f"mysql+pymysql://{username}:{password}@{hostname}/{database_name}"
    engine = create_engine(connection_str)
    query = f"SELECT * FROM {desired_table_name}"

    df = pd.read_sql(query, engine)

    return df


def import_from_excel(input_excel_data):
    sheet_names = ["corp_info", "bs", "incs", "cf"]

    df_dict = {}

    for sheet_name in sheet_names:
        df_dict[sheet_name] = pd.read_excel(
            input_excel_data, sheet_name, engine="openpyxl"
        )

    corp_info = df_dict["corp_info"]
    bs = df_dict["bs"]
    incs = df_dict["incs"]
    cf = df_dict["cf"]

    # initialization
    user = "multi"
    password = "Campus123!"
    host = "ec2-15-152-211-160.ap-northeast-3.compute.amazonaws.com"
    database = "Data_Mart"

    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

    query = "SELECT * FROM Data_Mart.industry_average_year;"
    industry_average = pd.read_sql(query, engine)

    query = "SELECT * FROM Data_Lake.crb_index;"
    crb_index = pd.read_sql(query, engine)

    query = "SELECT * FROM Data_Warehouse.economic_indicators;"
    economic_indicators = pd.read_sql(query, engine)

    query = "SELECT * FROM Data_Mart.credit_model_a;"
    model_a = pd.read_sql(query, engine)

    query = "SELECT * FROM Data_Mart.sector_revenue_top_features;"
    sector_revenue_top_features = pd.read_sql(query, engine)

    query = "SELECT * FROM Data_Mart.sector_revenue_aggregation;"
    sector_revenue_aggregation = pd.read_sql(query, engine)

    sector = corp_info["산업"][0]
    revenue = incs["계정값"][0]

    input_sectors = [sector]
    new_data = {sector: revenue}

    clustered_sectors = [
        "서비스업",
        "기타금융",
        "운수창고업",
        "음식료품",
        "화학",
        "전기전자",
        "유통업",
        "기계",
        "운수장비",
        "의약품",
        "철강금속",
    ]

    percentile_sectors = [
        "건설업",
        "섬유의복",
        "통신업",
        "전기가스업",
        "종이목재",
        "농업, 임업 및 어업",
        "비금속광물",
        "기타제조업",
    ]

    # import account_info

    corp = corp_info["기업이름"][0]
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
    outstanding_shares = corp_info["발행주식수"]
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
    ebitda_to_interest_expense = ebitda / interest * 100
    debt_ratio = total_liabilities / total_assets * 100
    dependence_on_net_borrowings = borrowings / total_equity * 100
    net_borrowings_to_ebitda = net_borrowings / ebitda * 100
    cogs = cost_of_sales
    selling_general_administrative_expenses = selling_general_administrative_expenses
    ebit = ebit
    ebit_margin = ebit / revenue * 100
    ebitda_to_sales_revenue = ebitda / revenue * 100
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
    borrowing_dependency = borrowings / total_equity * 100
    total_borrowings_to_ebitda = borrowings / ebitda * 100
    debt_to_net_income_ratio = total_liabilities / net_income * 100
    total_assets_leverage = total_assets / total_equity * 100
    current_liabilities = current_liabilities
    working_capital = current_assets - current_liabilities
    current_liabilities_ratio = current_liabilities / current_assets * 100
    quick_assets = quick_assets
    quick_ratio = quick_assets / current_liabilities * 100
    cash_and_cash_equivalents = cash_and_equivalents
    short_term_borrowings = short_borrowing
    days_sales_outstanding = accounts_receivable / revenue * 365
    market_capitalization = market_capitalization

    # 질적데이터 피쳐
    minimum_wage = model_a[model_a["year"] == "2022"]["minimum_wage"].values[0]
    us_kor_exchange_avg = model_a[model_a["year"] == "2022"][
        "us_kor_exchange_avg"
    ].values[0]
    ppi_year = model_a[model_a["year"] == "2022"]["ppi_year"].values[0]
    kor_usa_ir_diff = model_a[model_a["year"] == "2022"]["kor_usa_ir_diff"].values[0]
    kr_standard_yield = model_a[model_a["year"] == "2022"]["kr_standard_yield"].values[
        0
    ]
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
    culture = industry_average[industry_average["sector"] == sector]["culture"].values[
        0
    ]
    opportunity = industry_average[industry_average["sector"] == sector][
        "opportunity"
    ].values[0]
    manager = industry_average[industry_average["sector"] == sector]["manager"].values[
        0
    ]
    recommend = industry_average[industry_average["sector"] == sector][
        "recommend"
    ].values[0]
    ceo = industry_average[industry_average["sector"] == sector]["ceo"].values[0]
    potential = industry_average[industry_average["sector"] == sector][
        "potential"
    ].values[0]

    # 투자지표 피쳐
    earnings_per_share = net_income / outstanding_shares
    book_value_per_share = total_equity / outstanding_shares

    gross_profit_margin = gross_profit / revenue * 100
    operating_profit_margin = operating_income / revenue * 100
    net_profit_margin = net_income / revenue * 100
    ebitda_margin = ebitda / revenue * 100
    return_on_equity = net_income / total_equity * 100
    return_on_assets = net_income / total_assets * 100
    return_on_invested_capital = (
        operating_income / (total_equity + total_liabilities) * 100
    )

    debt_ratio = total_liabilities / total_assets * 100
    current_ratio = current_assets / current_liabilities * 100
    quick_ratio = (current_assets - inventory) / current_liabilities * 100
    non_current_debt_ratio = non_current_liabilities / total_assets * 100
    equity_ratio = total_equity / total_assets * 100
    interest_coverage_ratio = ebit / interest * 100
    debt_to_equity_ratio = total_liabilities / total_equity * 100
    net_debt_ratio = (borrowings - cash_and_equivalents) / total_assets * 100
    retention_ratio = retained_earnings / net_income * 100

    earnings_per_share = net_income / outstanding_shares
    book_value_per_share = total_equity / outstanding_shares
    price_earnings_ratio = stock_price / earnings_per_share
    price_to_book_ratio = stock_price / book_value_per_share
    price_cash_flow_ratio = stock_price / (cash_flow_operating / outstanding_shares)
    enterprise_value_to_ebitda = (
        market_capitalization + borrowings - cash_and_equivalents
    ) / ebitda

    market_capitalization = market_capitalization

    total_asset_turnover = revenue / total_assets * 100
    return_on_equity = net_income / total_equity * 100
    net_working_capital_turnover = (
        revenue / (current_assets - current_liabilities) * 100
    )
    tangible_asset_turnover = revenue / tangible_assets * 100
    accounts_receivable_turnover = revenue / accounts_receivable * 100
    inventory_turnover = cost_of_sales / inventory * 100
    accounts_payable_turnover = cost_of_sales / accounts_payable * 100

    data_jaemu = pd.DataFrame(
        {
            "corp": [corp],
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
        }
    )

    return data_jaemu


def merge_data(data_reviews, data_jaemu):
    data_reviews = data_reviews[
        data_reviews["corp"] == data_jaemu["corp"].values.astype("str")[0]
    ]
    data_else = data_jaemu.copy()

    data_total = pd.merge(data_reviews, data_jaemu, on="corp", how="inner")

    if len(data_total) == 0:
        return data_jaemu.copy()

    else:
        return data_total
