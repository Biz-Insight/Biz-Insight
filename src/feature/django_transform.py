import warnings
import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import numpy as np
import pickle
from scipy import stats

warnings.filterwarnings("ignore", category=FutureWarning)


def django_transform(fs):
    ###############################################################################
    # Django fs

    # sheet_names = fs.sheet_names

    # df_dict = {}

    # for sheet_name in sheet_names:
    #     df_dict[sheet_name] = pd.read_excel(fs, sheet_name, engine="openpyxl")

    # corp_info = df_dict["corp_info"]
    # bs = df_dict["bs"]
    # incs = df_dict["incs"]
    # cf = df_dict["cf"]
    ###############################################################################
    # No Django fs
    corp_info = fs["corp_info"]
    bs = fs["bs"]
    incs = fs["incs"]
    cf = fs["cf"]
    ###############################################################################
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

    ###############################################################################

    sector = corp_info["산업"][0]
    revenue = incs["Value"][0]

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

    with open("cluster_label_mappings.pkl", "rb") as f:
        cluster_label_mappings = pickle.load(f)

    with open("sector_revenue_data.pkl", "rb") as f:
        sector_revenue_data = pickle.load(f)

    for sector in input_sectors:
        if sector in clustered_sectors:
            with open(f"{sector}_kmeans_model.pkl", "rb") as file:
                model = pickle.load(file)

            data = new_data[sector]
            data_array = np.array([[data]])
            cluster_label = model.predict(data_array)[0]
            revenue_group = cluster_label_mappings[sector][cluster_label]
        elif sector in percentile_sectors:
            data = new_data[sector]
            data_of_sector = np.array(sector_revenue_data[sector])
            percentile = stats.percentileofscore(data_of_sector, data)
            if percentile < 33:
                print(f"The data of {sector} belongs to group 하위")
                revenue_group = "하위"
            elif percentile < 67:
                print(f"The data of {sector} belongs to group 중위")
                revenue_group = "중위"
            else:
                print(f"The data of {sector} belongs to group 상위")
                revenue_group = "상위"
        else:
            print(f"Unknown sector: {sector}")

    ###############################################################################
    # credit_group_prediction
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
    ###############################################################################
    # model_with_y = (
    #     model_a[model_a["rank"].notna()]
    #     .reset_index(drop=True)
    #     .drop(["corp", "stock_code", "sector", "year"], axis=1)
    # )
    # model_without_y = (
    #     model_a[model_a["rank"].isna()].reset_index(drop=True).drop(["rank"], axis=1)
    # )

    # # 선정한 모델
    # X = model_with_y.drop("rank", axis=1)
    # y = model_with_y["rank"]
    # y = y.map(rank_mapping)

    # X_train, X_test, y_train, y_test = train_test_split(
    #     X, y, test_size=0.2, random_state=42
    # )

    # clf = RandomForestClassifier(
    #     criterion="entropy",
    #     max_depth=18,
    #     max_features="sqrt",
    #     n_estimators=500,
    #     random_state=42,
    # )
    # clf.fit(X_train, y_train)

    # with open("rf_model.pkl", "wb") as file:
    #     pickle.dump(clf, file)
    ###############################################################################
    with open("rf_model.pkl", "rb") as file:
        clf = pickle.load(file)

    ###############################################################################

    # 액셀에서 계정 값 받아오기
    corp_name = corp_info["기업이름"][0]
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
    stock_price = corp_info["현재주가"]
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

    # 예측을 위한 데이터 데이터프레임으로 변경
    group_prediction_data = pd.DataFrame(
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
        }
    )

    rank_group_prediction = clf.predict(group_prediction_data)
    rank_mapping_reverse = {v: k for k, v in rank_mapping.items()}
    credit_group_prediction = rank_mapping_reverse[rank_group_prediction[0]]

    ###############################################################################
    # main_fs

    mapping = {
        "total_assets": ("bs", corp_name, sector, "자산총계"),
        "tangible_assets": ("bs", corp_name, sector, "유형자산"),
        "intangible_assets": ("bs", corp_name, sector, "무형자산"),
        "cash_and_equivalents": ("bs", corp_name, sector, "현금및현금성자산"),
        "total_equity": ("bs", corp_name, sector, "자본총계"),
        "total_liabilities": ("bs", corp_name, sector, "부채총계"),
        "revenue": ("incs", corp_name, sector, "매출액"),
        "cost_of_sales": ("incs", corp_name, sector, "매출원가"),
        "selling_general_administrative_expenses": (
            "incs",
            corp_name,
            sector,
            "판매비와관리비",
        ),
        "operating_income": ("incs", corp_name, sector, "영업이익"),
        "net_income": ("incs", corp_name, sector, "당기순이익"),
        "cash_flow_operating": ("cf", corp_name, sector, "영업활동현금흐름"),
        "cash_flow_investing": ("cf", corp_name, sector, "투자활동현금흐름"),
        "cash_flow_financing": ("cf", corp_name, sector, "재무활동현금흐름"),
    }

    values = [
        total_assets,
        tangible_assets,
        intangible_assets,
        cash_and_equivalents,
        total_equity,
        total_liabilities,
        revenue,
        cost_of_sales,
        selling_general_administrative_expenses,
        operating_income,
        net_income,
        cash_flow_operating,
        cash_flow_investing,
        cash_flow_financing,
    ]

    main_fs_data = []

    for label, value in zip(mapping.keys(), values):
        fs_type, corp, sector, label_ko = mapping[label]
        main_fs_data.append([fs_type, corp, sector, label, label_ko, value])

    main_fs = pd.DataFrame(
        main_fs_data,
        columns=["fs_type", "corp", "sector", "label_en", "label_ko", "current year"],
    )

    # main_fs['industry_avg'] = industry_average[industry_average['sector']==sector][main_fs[label_en]]

    ###############################################################################
    # credit_data_web

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

    values_dict = {
        "ebitda_margin": ebitda_margin,
        "ebitda_to_interest_expense": ebitda_to_interest_expense,
        "debt_ratio": debt_ratio,
        "dependence_on_net_borrowings": dependence_on_net_borrowings,
        "operating_cf_to_total_borrowings": cash_flow_operating / total_borrowings,
        "net_borrowings_to_ebitda": net_borrowings_to_ebitda,
        "revenue": revenue,
        "cogs": cost_of_sales,
        "selling_general_administrative_expenses": selling_general_administrative_expenses,
        "ebit": ebit,
        "ebit_margin": ebit_margin,
        "ebitda_to_sales_revenue": ebitda_to_sales_revenue,
        "total_assets": total_assets,
        "return_on_assets": return_on_assets,
        "ebitda": ebitda,
        "financial_expenses": financial_expenses,
        "corporate_tax": corporate_tax,
        "operating_cash_flow": operating_cash_flow,
        "free_cash_flow": free_cash_flow,
        "total_liabilities": total_liabilities,
        "total_equity": total_equity,
        "total_borrowings": total_borrowings,
        "net_borrowings": net_borrowings,
        "borrowing_dependency": borrowing_dependency,
        "total_borrowings_to_ebitda": total_borrowings_to_ebitda,
        "debt_to_net_income_ratio": debt_to_net_income_ratio,
        "total_assets_leverage": total_assets_leverage,
        "current_liabilities": current_liabilities,
        "working_capital": working_capital,
        "current_liabilities_ratio": current_liabilities_ratio,
        "quick_assets": quick_assets,
        "quick_ratio": quick_ratio,
        "cash_and_cash_equivalents": cash_and_cash_equivalents,
        "short_term_borrowings": short_term_borrowings,
        "cash_and_cash_equivalents_to_short_term_borrowings_ratio": cash_and_cash_equivalents
        / short_term_borrowings
        * 100,
        "short_term_borrowings_to_total_borrowings_ratio": short_term_borrowings
        / total_borrowings
        * 100,
        "days_sales_outstanding": days_sales_outstanding,
        "market_capitalization": market_capitalization,
    }

    credit_data_web = pd.DataFrame(
        columns=["corp", "sector", "label_en", "label_ko", "current_year"]
    )

    for label_en, label_ko in mapping.items():
        credit_data_web = credit_data_web.append(
            {
                "corp": corp_name,
                "sector": sector,
                "label_en": label_en,
                "label_ko": label_ko,
                "current_year": values_dict.get(label_en, None),
            },
            ignore_index=True,
        )

    ###############################################################################
    # investment_data_web

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
        "total_asset_turnover": "총자산회전율",
        "net_working_capital_turnover": "순운전자본회전율",
        "tangible_asset_turnover": "유형자산회전율",
        "accounts_receivable_turnover": "매출채권회전율",
        "inventory_turnover": "재고자산회전율",
        "accounts_payable_turnover": "매입채무회전율",
        "market_capitalization": "시가총액",
    }

    values_dict = {
        "gross_profit_margin": gross_profit_margin,
        "operating_profit_margin": operating_profit_margin,
        "net_profit_margin": net_profit_margin,
        "ebitda_margin": ebitda_margin,
        "return_on_equity": return_on_equity,
        "return_on_assets": return_on_assets,
        "return_on_invested_capital": return_on_invested_capital,
        "debt_ratio": debt_ratio,
        "current_ratio": current_ratio,
        "quick_ratio": quick_ratio,
        "non_current_debt_ratio": non_current_debt_ratio,
        "equity_ratio": equity_ratio,
        "interest_coverage_ratio": interest_coverage_ratio,
        "debt_to_equity_ratio": debt_to_equity_ratio,
        "net_debt_ratio": net_debt_ratio,
        "retention_ratio": retention_ratio,
        "earnings_per_share": earnings_per_share,
        "book_value_per_share": book_value_per_share,
        "price_earnings_ratio": book_value_per_share,
        "price_to_book_ratio": price_to_book_ratio,
        "price_cash_flow_ratio": price_cash_flow_ratio,
        "enterprise_value_to_ebitda": enterprise_value_to_ebitda,
        "total_asset_turnover": total_asset_turnover,
        "net_working_capital_turnover": net_working_capital_turnover,
        "tangible_asset_turnover": tangible_asset_turnover,
        "accounts_receivable_turnover": accounts_receivable_turnover,
        "inventory_turnover": inventory_turnover,
        "accounts_payable_turnover": accounts_payable_turnover,
        "market_capitalization": market_capitalization,
    }

    investment_data_web = pd.DataFrame(
        columns=["corp", "sector", "label_en", "label_ko", "current_year"]
    )

    for label_en, label_ko in mapping.items():
        investment_data_web = investment_data_web.append(
            {
                "corp": corp_name,
                "sector": sector,
                "label_en": label_en,
                "label_ko": label_ko,
                "current_year": values_dict.get(label_en, None),
            },
            ignore_index=True,
        )

    ###############################################################################
    # update main_fs, credit_data_web, investment_data_web

    corp_average = industry_average[industry_average["sector"] == sector]

    corp_average = corp_average.set_index("sector")

    def get_value(row):
        sector, label = row["sector"], row["label_en"]
        if label in corp_average.columns:
            return corp_average.at[sector, label]
        return None

    main_fs["industry_avg"] = main_fs.apply(get_value, axis=1)
    credit_data_web["industry_avg"] = credit_data_web.apply(get_value, axis=1)
    investment_data_web["industry_avg"] = investment_data_web.apply(get_value, axis=1)

    sector_revenue_aggregation.columns = sector_revenue_aggregation.columns.str.lower()

    corp_agg = sector_revenue_aggregation[
        (sector_revenue_aggregation["sector"] == sector)
        & (sector_revenue_aggregation["revenue_group"] == revenue_group)
    ]

    def populate_cluster_values(
        main_df: pd.DataFrame, agg_df: pd.DataFrame
    ) -> pd.DataFrame:
        main_df["cluster_max"] = np.nan
        main_df["cluster_median"] = np.nan
        main_df["cluster_min"] = np.nan

        for label in main_df["label_en"].unique():
            max_col = label + "_max"
            median_col = label + "_median"
            min_col = label + "_min"

            if (
                max_col not in agg_df.columns
                or median_col not in agg_df.columns
                or min_col not in agg_df.columns
            ):
                continue

            temp_df = main_df[main_df["label_en"] == label].merge(
                agg_df[["sector", max_col, median_col, min_col]],
                on="sector",
                how="left",
            )

            main_df.loc[main_df["label_en"] == label, "cluster_max"] = temp_df[
                max_col
            ].values
            main_df.loc[main_df["label_en"] == label, "cluster_median"] = temp_df[
                median_col
            ].values
            main_df.loc[main_df["label_en"] == label, "cluster_min"] = temp_df[
                min_col
            ].values

        return main_df

    main_fs = populate_cluster_values(main_fs, corp_agg)
    credit_data_web = populate_cluster_values(credit_data_web, corp_agg)
    investment_data_web = populate_cluster_values(investment_data_web, corp_agg)

    ###############################################################################
    # top_correlation - top 5 correlation

    credit_data_web = credit_data_web[
        ~credit_data_web["label_en"].isin(main_fs["label_en"])
    ]
    investment_data_web = investment_data_web[
        ~investment_data_web["label_en"].isin(main_fs["label_en"])
    ]

    combined_df = pd.concat([credit_data_web, investment_data_web], ignore_index=True)

    combined_df_unique = combined_df.drop_duplicates(subset="label_en", keep="first")

    cluster_df = pd.concat([main_fs, combined_df_unique], ignore_index=True)

    corp_row = sector_revenue_top_features[
        (sector_revenue_top_features["Sector"] == sector)
        & (sector_revenue_top_features["Revenue_Group"] == revenue_group)
    ]

    corr_df = []

    for idx, row in corp_row.iterrows():
        for i in range(1, 6):
            feature = row[f"Top{i}"]
            correlation = row[f"Correlation{i}"]

            corr_df.append(
                {
                    "feature": feature.lower(),
                    "correlation": correlation,
                    "sector": row["Sector"],
                    "revenue_group": row["Revenue_Group"],
                    "corp_value": locals().get(feature.lower(), None),
                    "industry_average": industry_average[
                        industry_average["sector"] == sector
                    ][feature.lower()].values[0],
                    "cluster_max": cluster_df[
                        cluster_df["label_en"] == feature.lower()
                    ]["cluster_max"].values[0],
                    "cluster_median": cluster_df[
                        cluster_df["label_en"] == feature.lower()
                    ]["cluster_median"].values[0],
                    "cluster_min": cluster_df[
                        cluster_df["label_en"] == feature.lower()
                    ]["cluster_min"].values[0],
                }
            )
    top_correlation = pd.DataFrame(corr_df)

    ###############################################################################
    # sector_credit_rating

    sector_filter = sector_revenue_aggregation[
        sector_revenue_aggregation["sector"] == sector
    ]
    sector_credit_rating = sector_filter[
        ["sector", "revenue_group", "rank_value_median"]
    ].reset_index(drop=True)

    ###############################################################################
    return (
        credit_group_prediction,
        main_fs,
        credit_data_web,
        investment_data_web,
        top_correlation,
        sector_credit_rating,
    )


fs = pd.read_excel("Credit_Prediction.xlsx", sheet_name=None)

(
    credit_group_prediction,
    main_fs,
    credit_data_web,
    investment_data_web,
    top_correlation,
    sector_credit_rating,
) = django_transform(fs)

print(credit_group_prediction)
