# Generated by Django 2.1.7 on 2023-07-24 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_companyinvestment_industryinvestment'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndustryAverage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector', models.TextField(blank=True, null=True)),
                ('ebitda_margin', models.FloatField(blank=True, null=True)),
                ('ebitda_to_interest_expense', models.FloatField(blank=True, null=True)),
                ('debt_ratio', models.FloatField(blank=True, null=True)),
                ('dependence_on_net_borrowings', models.FloatField(blank=True, null=True)),
                ('net_borrowings_to_ebitda', models.FloatField(blank=True, null=True)),
                ('revenue', models.FloatField(blank=True, null=True)),
                ('cogs', models.FloatField(blank=True, null=True)),
                ('selling_general_administrative_expenses', models.FloatField(blank=True, null=True)),
                ('ebit', models.FloatField(blank=True, null=True)),
                ('ebit_margin', models.FloatField(blank=True, null=True)),
                ('ebitda_to_sales_revenue', models.FloatField(blank=True, null=True)),
                ('total_assets', models.FloatField(blank=True, null=True)),
                ('return_on_assets', models.FloatField(blank=True, null=True)),
                ('ebitda', models.FloatField(blank=True, null=True)),
                ('financial_expenses', models.FloatField(blank=True, null=True)),
                ('corporate_tax', models.FloatField(blank=True, null=True)),
                ('operating_cash_flow', models.FloatField(blank=True, null=True)),
                ('free_cash_flow', models.FloatField(blank=True, null=True)),
                ('total_liabilities', models.FloatField(blank=True, null=True)),
                ('total_equity', models.FloatField(blank=True, null=True)),
                ('total_borrowings', models.FloatField(blank=True, null=True)),
                ('net_borrowings', models.FloatField(blank=True, null=True)),
                ('borrowing_dependency', models.FloatField(blank=True, null=True)),
                ('total_borrowings_to_ebitda', models.FloatField(blank=True, null=True)),
                ('debt_to_net_income_ratio', models.FloatField(blank=True, null=True)),
                ('total_assets_leverage', models.FloatField(blank=True, null=True)),
                ('current_liabilities', models.FloatField(blank=True, null=True)),
                ('working_capital', models.FloatField(blank=True, null=True)),
                ('current_liabilities_ratio', models.FloatField(blank=True, null=True)),
                ('quick_assets', models.FloatField(blank=True, null=True)),
                ('quick_ratio', models.FloatField(blank=True, null=True)),
                ('cash_and_cash_equivalents', models.FloatField(blank=True, null=True)),
                ('short_term_borrowings', models.FloatField(blank=True, null=True)),
                ('days_sales_outstanding', models.FloatField(blank=True, null=True)),
                ('market_capitalization', models.FloatField(blank=True, null=True)),
                ('minimum_wage', models.FloatField(blank=True, null=True)),
                ('us_kor_exchange_avg', models.FloatField(blank=True, null=True)),
                ('ppi_year', models.FloatField(blank=True, null=True)),
                ('kor_usa_ir_diff', models.FloatField(blank=True, null=True)),
                ('kr_standard_yield', models.FloatField(blank=True, null=True)),
                ('count', models.FloatField(blank=True, null=True)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('paywellfare', models.FloatField(blank=True, null=True)),
                ('worklifebal', models.FloatField(blank=True, null=True)),
                ('culture', models.FloatField(blank=True, null=True)),
                ('opportunity', models.FloatField(blank=True, null=True)),
                ('manager', models.FloatField(blank=True, null=True)),
                ('recommend', models.FloatField(blank=True, null=True)),
                ('ceo', models.FloatField(blank=True, null=True)),
                ('potential', models.FloatField(blank=True, null=True)),
                ('crb_index_avg', models.FloatField(blank=True, null=True)),
                ('gross_profit_margin', models.FloatField(blank=True, null=True)),
                ('operating_profit_margin', models.FloatField(blank=True, null=True)),
                ('net_profit_margin', models.FloatField(blank=True, null=True)),
                ('return_on_equity', models.FloatField(blank=True, null=True)),
                ('return_on_invested_capital', models.FloatField(blank=True, null=True)),
                ('current_ratio', models.FloatField(blank=True, null=True)),
                ('non_current_debt_ratio', models.FloatField(blank=True, null=True)),
                ('equity_ratio', models.FloatField(blank=True, null=True)),
                ('interest_coverage_ratio', models.FloatField(blank=True, null=True)),
                ('debt_to_equity_ratio', models.FloatField(blank=True, null=True)),
                ('net_debt_ratio', models.FloatField(blank=True, null=True)),
                ('retention_ratio', models.FloatField(blank=True, null=True)),
                ('earnings_per_share', models.FloatField(blank=True, null=True)),
                ('book_value_per_share', models.FloatField(blank=True, null=True)),
                ('price_earnings_ratio', models.FloatField(blank=True, null=True)),
                ('price_to_book_ratio', models.FloatField(blank=True, null=True)),
                ('price_cash_flow_ratio', models.FloatField(blank=True, null=True)),
                ('enterprise_value_to_ebitda', models.FloatField(blank=True, null=True)),
                ('operating_income', models.FloatField(blank=True, null=True)),
                ('net_income', models.FloatField(blank=True, null=True)),
                ('tangible_assets', models.FloatField(blank=True, null=True)),
                ('total_asset_turnover', models.FloatField(blank=True, null=True)),
                ('net_working_capital_turnover', models.FloatField(blank=True, null=True)),
                ('tangible_asset_turnover', models.FloatField(blank=True, null=True)),
                ('accounts_receivable_turnover', models.FloatField(blank=True, null=True)),
                ('inventory_turnover', models.FloatField(blank=True, null=True)),
                ('accounts_payable_turnover', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'industry_average',
            },
        ),
    ]