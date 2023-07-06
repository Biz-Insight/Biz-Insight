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

    def __str__(self):
        return self.stock_code

    class Meta:
        db_table = "credit_mockup"
