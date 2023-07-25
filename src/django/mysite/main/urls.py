from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("company_list/", views.CompanyList.as_view(), name="company_list"),
    path("search/", views.search_view, name="search"),
    path("get_gpt_summary/", views.get_gpt_summary_view, name="get_gpt_summary"),
    path(
        "company_info/<str:company_name>/",
        views.CompanyInfoWeb.as_view(),
        name="company_info",
    ),
    path(
        "company_news/<str:company_name>/",
        views.CompanyNews.as_view(),
        name="company_news",
    ),
    path(
        "financial_analysis/<str:company_name>/",
        views.FinancialAnalysis.as_view(),
        name="financial_analysis",
    ),
    path(
        "credit_analysis/<str:company_name>/",
        views.CreditAnalysis.as_view(),
        name="credit_analysis",
    ),
    path(
        "financial_statements/<str:company_name>/",
        views.MainFinancialStatements.as_view(),
        name="financial_statements",
    ),
    path(
        "investment_indicator/<str:company_name>/",
        views.InvestmentIndicator.as_view(),
        name="investment_indicator",
    ),
    path(
        "credit_indicator/<str:company_name>/",
        views.CreditIndicator.as_view(),
        name="credit_indicator",
    ),
    path(
        "chart_data/<str:chart_type>/",
        views.ChartData.as_view(),
        name="chart_data",
    ),
    path("stock_area/", views.StockArea.as_view(), name="stock_area"),
    path("credit_request/", views.credit_request),
    path("new_company_info/", views.new_company_info, name="new_company_info"),
    path("new_company_news/", views.new_company_news, name="new_company_news"),
    path("new_credit_analysis/", views.new_credit_analysis, name="new_credit_analysis"),
    path(
        "new_credit_indicator/", views.new_credit_indicator, name="new_credit_indicator"
    ),
    path(
        "new_financial_analysis/",
        views.new_financial_analysis,
        name="new_financial_analysis",
    ),
    path(
        "new_financial_statements/",
        views.new_financial_statements,
        name="new_financial_statements",
    ),
    path(
        "new_investment_indicator/",
        views.new_investment_indicator,
        name="new_investment_indicator",
    ),
]
