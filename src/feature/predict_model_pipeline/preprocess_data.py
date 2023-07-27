from import_data import *


def padding_sequences(data, up_or_down, max_length):
    up_or_down = up_or_down + "_sp"

    data = data.drop(data[data[up_or_down].isna() == True].index)

    data[up_or_down] = data[up_or_down].apply(
        lambda x: [int(i) for i in re.findall(r"\d+", x)]
    )

    sequences_reviews = pad_sequences(
        data[up_or_down], maxlen=max_length, padding="post", truncating="post"
    )
    return sequences_reviews


def jaemu_data_preprocessing(data):
    with open("./scaler.pkl", "rb") as file:
        scaler = pickle.load(file)

    scaled_data_jaemu = scaler.transform(
        data[
            [
                "ebitda_margin",
                "ebitda_to_interest_expense",
                "debt_ratio",
                "dependence_on_net_borrowings",
                "net_borrowings_to_ebitda",
                "revenue",
                "cogs",
                "selling_general_administrative_expenses",
                "ebit",
                "ebit_margin",
                "ebitda_to_sales_revenue",
                "total_assets",
                "return_on_assets",
                "ebitda",
                "financial_expenses",
                "corporate_tax",
                "operating_cash_flow",
                "free_cash_flow",
                "total_liabilities",
                "total_equity",
                "total_borrowings",
                "net_borrowings",
                "borrowing_dependency",
                "total_borrowings_to_ebitda",
                "debt_to_net_income_ratio",
                "total_assets_leverage",
                "current_liabilities",
                "working_capital",
                "current_liabilities_ratio",
                "quick_assets",
                "quick_ratio",
                "cash_and_cash_equivalents",
                "short_term_borrowings",
                "days_sales_outstanding",
                "market_capitalization",
                "minimum_wage",
                "us_kor_exchange_avg",
                "ppi_year",
                "kor_usa_ir_diff",
                "kr_standard_yield",
                "count",
                "rating",
                "paywellfare",
                "worklifebal",
                "culture",
                "opportunity",
                "manager",
                "recommend",
                "ceo",
                "potential",
                "crb_index_avg",
            ]
        ]
    )

    return scaled_data_jaemu
