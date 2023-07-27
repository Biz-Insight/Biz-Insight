from django.db import models

# from sklearn.ensemble import RandomForestClassifier
# import joblib


class CisDf(models.Model):
    corp = models.TextField(blank=True, null=True)
    account = models.TextField(blank=True, null=True)
    account_detail = models.TextField(blank=True, null=True)
    account_detail_2 = models.TextField(blank=True, null=True)
    number_2018 = models.FloatField(db_column="2018", blank=True, null=True)
    number_2019 = models.FloatField(db_column="2019", blank=True, null=True)
    number_2020 = models.FloatField(db_column="2020", blank=True, null=True)
    number_2021 = models.FloatField(db_column="2021", blank=True, null=True)
    number_2022 = models.FloatField(db_column="2022", blank=True, null=True)

    class Meta:
        db_table = "cis_df"


class StockDay(models.Model):
    corp = models.TextField(blank=True, null=True)
    stock_code = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    open_price = models.FloatField(blank=True, null=True)
    high_price = models.FloatField(blank=True, null=True)
    low_price = models.FloatField(blank=True, null=True)
    close_price = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    foreign_ownership_ratio = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = "stock_data_per_day"


class CompanyName(models.Model):
    standard_code = models.CharField(
        db_column="Standard_code", unique=True, max_length=20
    )
    short_code = models.TextField(db_column="Short_code", blank=True, null=True)
    company_full_name = models.TextField(
        db_column="Company_full_name", blank=True, null=True
    )
    company_name = models.TextField(db_column="Company_name", blank=True, null=True)

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = "company_name"


class MainFs(models.Model):
    fs_type = models.TextField(blank=True, null=True)
    corp = models.TextField(blank=True, null=True)
    stock_code = models.TextField(blank=True, null=True)
    sector = models.TextField(blank=True, null=True)
    label_en = models.TextField(blank=True, null=True)
    label_ko = models.TextField(blank=True, null=True)
    number_2018 = models.FloatField(db_column="2018", blank=True, null=True)
    number_2019 = models.FloatField(db_column="2019", blank=True, null=True)
    number_2020 = models.FloatField(db_column="2020", blank=True, null=True)
    number_2021 = models.FloatField(db_column="2021", blank=True, null=True)
    number_2022 = models.FloatField(db_column="2022", blank=True, null=True)
    yoy = models.FloatField(db_column="YoY", blank=True, null=True)

    class Meta:
        db_table = "main_fs"


class InvestmentData(models.Model):
    corp = models.TextField(blank=True, null=True)
    stock_code = models.TextField(blank=True, null=True)
    sector = models.TextField(blank=True, null=True)
    label_en = models.TextField(blank=True, null=True)
    label_ko = models.TextField(blank=True, null=True)
    number_2018 = models.FloatField(db_column="2018", blank=True, null=True)
    number_2019 = models.FloatField(db_column="2019", blank=True, null=True)
    number_2020 = models.FloatField(db_column="2020", blank=True, null=True)
    number_2021 = models.FloatField(db_column="2021", blank=True, null=True)
    number_2022 = models.FloatField(db_column="2022", blank=True, null=True)
    yoy = models.FloatField(db_column="YoY", blank=True, null=True)

    class Meta:
        db_table = "investment_data"


class CreditData(models.Model):
    corp = models.TextField(blank=True, null=True)
    stock_code = models.TextField(blank=True, null=True)
    sector = models.TextField(blank=True, null=True)
    label_en = models.TextField(blank=True, null=True)
    label_ko = models.TextField(blank=True, null=True)
    number_2018 = models.FloatField(db_column="2018", blank=True, null=True)
    number_2019 = models.FloatField(db_column="2019", blank=True, null=True)
    number_2020 = models.FloatField(db_column="2020", blank=True, null=True)
    number_2021 = models.FloatField(db_column="2021", blank=True, null=True)
    number_2022 = models.FloatField(db_column="2022", blank=True, null=True)
    yoy = models.FloatField(db_column="YoY", blank=True, null=True)

    class Meta:
        db_table = "credit_data"


class Visualization(models.Model):
    corp = models.TextField(blank=True, null=True)
    stock_code = models.TextField(blank=True, null=True)
    sector = models.TextField(blank=True, null=True)
    label_en = models.TextField(blank=True, null=True)
    label_ko = models.TextField(blank=True, null=True)
    number_2018 = models.FloatField(db_column="2018", blank=True, null=True)
    number_2019 = models.FloatField(db_column="2019", blank=True, null=True)
    number_2020 = models.FloatField(db_column="2020", blank=True, null=True)
    number_2021 = models.FloatField(db_column="2021", blank=True, null=True)
    number_2022 = models.FloatField(db_column="2022", blank=True, null=True)
    yoy = models.FloatField(db_column="YoY", blank=True, null=True)

    class Meta:
        db_table = "visualization_data"


class CompanyInvestment(models.Model):
    corp = models.TextField(blank=True, null=True)
    sector = models.TextField(blank=True, null=True)
    profitability = models.FloatField(blank=True, null=True)
    growth = models.FloatField(blank=True, null=True)
    stability = models.FloatField(blank=True, null=True)
    activity = models.FloatField(blank=True, null=True)
    valuation = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = "company_investment"


class IndustryInvestment(models.Model):
    sector = models.TextField(blank=True, null=True)
    profitability = models.FloatField(blank=True, null=True)
    growth = models.FloatField(blank=True, null=True)
    stability = models.FloatField(blank=True, null=True)
    activity = models.FloatField(blank=True, null=True)
    valuation = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = "industry_investment"


class IndustryAverage(models.Model):
    sector = models.TextField(blank=True, null=True)
    ebitda_margin = models.FloatField(blank=True, null=True)
    ebitda_to_interest_expense = models.FloatField(blank=True, null=True)
    debt_ratio = models.FloatField(blank=True, null=True)
    dependence_on_net_borrowings = models.FloatField(blank=True, null=True)
    net_borrowings_to_ebitda = models.FloatField(blank=True, null=True)
    revenue = models.FloatField(blank=True, null=True)
    cogs = models.FloatField(blank=True, null=True)
    selling_general_administrative_expenses = models.FloatField(blank=True, null=True)
    ebit = models.FloatField(blank=True, null=True)
    ebit_margin = models.FloatField(blank=True, null=True)
    ebitda_to_sales_revenue = models.FloatField(blank=True, null=True)
    total_assets = models.FloatField(blank=True, null=True)
    return_on_assets = models.FloatField(blank=True, null=True)
    ebitda = models.FloatField(blank=True, null=True)
    financial_expenses = models.FloatField(blank=True, null=True)
    corporate_tax = models.FloatField(blank=True, null=True)
    operating_cash_flow = models.FloatField(blank=True, null=True)
    free_cash_flow = models.FloatField(blank=True, null=True)
    total_liabilities = models.FloatField(blank=True, null=True)
    total_equity = models.FloatField(blank=True, null=True)
    total_borrowings = models.FloatField(blank=True, null=True)
    net_borrowings = models.FloatField(blank=True, null=True)
    borrowing_dependency = models.FloatField(blank=True, null=True)
    total_borrowings_to_ebitda = models.FloatField(blank=True, null=True)
    debt_to_net_income_ratio = models.FloatField(blank=True, null=True)
    total_assets_leverage = models.FloatField(blank=True, null=True)
    current_liabilities = models.FloatField(blank=True, null=True)
    working_capital = models.FloatField(blank=True, null=True)
    current_liabilities_ratio = models.FloatField(blank=True, null=True)
    quick_assets = models.FloatField(blank=True, null=True)
    quick_ratio = models.FloatField(blank=True, null=True)
    cash_and_cash_equivalents = models.FloatField(blank=True, null=True)
    short_term_borrowings = models.FloatField(blank=True, null=True)
    days_sales_outstanding = models.FloatField(blank=True, null=True)
    market_capitalization = models.FloatField(blank=True, null=True)
    minimum_wage = models.FloatField(blank=True, null=True)
    us_kor_exchange_avg = models.FloatField(blank=True, null=True)
    ppi_year = models.FloatField(blank=True, null=True)
    kor_usa_ir_diff = models.FloatField(blank=True, null=True)
    kr_standard_yield = models.FloatField(blank=True, null=True)
    count = models.FloatField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    paywellfare = models.FloatField(blank=True, null=True)
    worklifebal = models.FloatField(blank=True, null=True)
    culture = models.FloatField(blank=True, null=True)
    opportunity = models.FloatField(blank=True, null=True)
    manager = models.FloatField(blank=True, null=True)
    recommend = models.FloatField(blank=True, null=True)
    ceo = models.FloatField(blank=True, null=True)
    potential = models.FloatField(blank=True, null=True)
    crb_index_avg = models.FloatField(blank=True, null=True)
    gross_profit_margin = models.FloatField(blank=True, null=True)
    operating_profit_margin = models.FloatField(blank=True, null=True)
    net_profit_margin = models.FloatField(blank=True, null=True)
    return_on_equity = models.FloatField(blank=True, null=True)
    return_on_invested_capital = models.FloatField(blank=True, null=True)
    current_ratio = models.FloatField(blank=True, null=True)
    non_current_debt_ratio = models.FloatField(blank=True, null=True)
    equity_ratio = models.FloatField(blank=True, null=True)
    interest_coverage_ratio = models.FloatField(blank=True, null=True)
    debt_to_equity_ratio = models.FloatField(blank=True, null=True)
    net_debt_ratio = models.FloatField(blank=True, null=True)
    retention_ratio = models.FloatField(blank=True, null=True)
    earnings_per_share = models.FloatField(blank=True, null=True)
    book_value_per_share = models.FloatField(blank=True, null=True)
    price_earnings_ratio = models.FloatField(blank=True, null=True)
    price_to_book_ratio = models.FloatField(blank=True, null=True)
    price_cash_flow_ratio = models.FloatField(blank=True, null=True)
    enterprise_value_to_ebitda = models.FloatField(blank=True, null=True)
    operating_income = models.FloatField(blank=True, null=True)
    net_income = models.FloatField(blank=True, null=True)
    tangible_assets = models.FloatField(blank=True, null=True)
    total_asset_turnover = models.FloatField(blank=True, null=True)
    net_working_capital_turnover = models.FloatField(blank=True, null=True)
    tangible_asset_turnover = models.FloatField(blank=True, null=True)
    accounts_receivable_turnover = models.FloatField(blank=True, null=True)
    inventory_turnover = models.FloatField(blank=True, null=True)
    accounts_payable_turnover = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = "industry_average"


class KospiCompanyInfo(models.Model):
    corp = models.TextField(blank=True, null=True)
    stock_code = models.TextField(blank=True, null=True)
    sector = models.TextField(blank=True, null=True)
    main_product = models.TextField(blank=True, null=True)
    listing_date = models.DateField(blank=True, null=True)
    settlement_month = models.TextField(blank=True, null=True)
    representative_name = models.TextField(blank=True, null=True)
    homepage = models.TextField(blank=True, null=True)
    region = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "kospi_company_info"


class CompanyInfo(models.Model):
    corp = models.TextField(blank=True, null=True)
    stock_code = models.TextField(blank=True, null=True)
    sector = models.TextField(blank=True, null=True)
    main_product = models.TextField(blank=True, null=True)
    listing_date = models.DateField(blank=True, null=True)
    settlement_month = models.TextField(blank=True, null=True)
    representative_name = models.TextField(blank=True, null=True)
    homepage = models.TextField(blank=True, null=True)
    region = models.TextField(blank=True, null=True)
    rank = models.TextField(blank=True, null=True)
    predicted_rank = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "company_info"


class Rating(models.Model):
    corp = models.TextField(blank=True, null=True)
    stock_code = models.TextField(blank=True, null=True)
    count = models.FloatField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    paywellfare = models.FloatField(blank=True, null=True)
    worklifebal = models.FloatField(blank=True, null=True)
    culture = models.FloatField(blank=True, null=True)
    opportunity = models.FloatField(blank=True, null=True)
    manager = models.FloatField(blank=True, null=True)
    recommend = models.FloatField(blank=True, null=True)
    ceo = models.FloatField(blank=True, null=True)
    potential = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = "rating"


class MockupData(models.Model):
    corp = models.TextField(blank=True, null=True)
    stock_code = models.TextField(blank=True, null=False)
    sector = models.TextField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)
    revenue = models.FloatField(blank=True, null=True)
    cost_of_sales = models.FloatField(blank=True, null=True)
    gross_profit = models.FloatField(blank=True, null=True)
    operating_income = models.FloatField(blank=True, null=True)
    net_income = models.FloatField(blank=True, null=True)
    ebit = models.FloatField(blank=True, null=True)
    ebitda = models.FloatField(blank=True, null=True)
    total_equity = models.FloatField(blank=True, null=True)
    total_assets = models.FloatField(blank=True, null=True)
    total_liabilities = models.FloatField(blank=True, null=True)
    current_assets = models.FloatField(blank=True, null=True)
    current_liabilities = models.FloatField(blank=True, null=True)
    non_current_liabilities = models.FloatField(blank=True, null=True)
    short_borrowing = models.FloatField(blank=True, null=True)
    long_borrowing = models.FloatField(blank=True, null=True)
    cash_and_equivalents = models.FloatField(blank=True, null=True)
    retained_earnings = models.FloatField(blank=True, null=True)
    ppe = models.FloatField(blank=True, null=True)
    intangible_assets = models.FloatField(blank=True, null=True)
    accounts_receivable = models.FloatField(blank=True, null=True)
    inventory = models.FloatField(blank=True, null=True)
    accounts_payable = models.FloatField(blank=True, null=True)
    outstanding_shares = models.BigIntegerField(blank=True, null=True)
    cash_flow = models.FloatField(blank=True, null=True)
    borrowings = models.FloatField(blank=True, null=True)
    net_liabilities = models.FloatField(blank=True, null=True)
    fixed_assets = models.FloatField(blank=True, null=True)
    cash_flow_per_share = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = "credit_mockup"


class Score(models.Model):
    name = models.CharField(blank=True, null=False, max_length=20)
    score = models.FloatField(blank=True, null=True)


class PhoneNumber(models.Model):
    name = models.CharField(blank=True, null=False, max_length=20)
    phone_number = models.FloatField(blank=True, null=True)


class Address(models.Model):
    name = models.CharField(blank=True, null=False, max_length=20)
    address = models.CharField(blank=True, null=True, max_length=20)
