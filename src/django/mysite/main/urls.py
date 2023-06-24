from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("company_list/", views.CompanyList.as_view(), name="company_list"),
    path("search/", views.search_view, name="search"),
    path("company_info/", views.Companyinfo.as_view(), name="company_info"),
]
