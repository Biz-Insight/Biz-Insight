from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("company_list/", views.CompanyList.as_view(), name="company_list"),
    path("search/", views.search_view, name="search"),
    path(
        "company_info/<str:company_name>/",
        views.Companyinfo.as_view(),
        name="company_info",
    ),
    path(
        "financial_analysis/<str:company_name>/",
        views.FinancialAnalysis.as_view(),
        name="financial_analysis",
    ),
    path(
        "company_news/<str:company_name>/",
        views.CompanyNews.as_view(),
        name="company_news",
    ),
    path("chart_data/", views.ChartData.as_view(), name="chart_data"),
    path("stock_area/", views.StockArea.as_view(), name="stock_area"),
]
