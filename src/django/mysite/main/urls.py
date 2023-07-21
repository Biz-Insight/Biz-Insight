from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("company_list/", views.CompanyList.as_view(), name="company_list"),
    path("search/", views.search_view, name="search"),
    path(
        "company_info/<str:company_name>/",
        views.CompanyInfo.as_view(),
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
    path("result/", views.show_result, name="result"),
]
