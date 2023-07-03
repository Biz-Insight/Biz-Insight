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
    path("chart_data/", views.ChartData.as_view(), name="chart_data"),
]
