from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView
from .models import CompanyName, CisDf


def home(request):
    return render(request, "index.html")


def company_direct(request):
    return render(request, "company_list.html")


def search_view(request):
    company_name = request.GET.get("company_name", "")
    request.session["context"] = company_name
    return redirect("company_info", company_name=company_name)


class CompanyList(ListView):
    model = CompanyName
    template_name = "company_list.html"
    context_object_name = "company_list"


class Companyinfo(ListView):
    model = CompanyName
    template_name = "company_info.html"
    context_object_name = "company_info"

    def get_queryset(self):
        company_name = self.request.session.get("context")
        queryset = CompanyName.objects.filter(company_name=company_name)
        return queryset


class ChartView(ListView):
    model = CisDf
    template_name = "company_info.html"
    context_object_name = "chart_view"

    def get_queryset(self):
        company_name = self.kwargs.get("company_name")
        queryset = CisDf.objects.filter(corp=company_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company_name"] = self.kwargs.get("company_name")
        return context


# class CisDf(ListView):
#     model = CisDf
#     template_name = "company_info.html"
#     context_object_name = "cis_df"

#     def get_queryset(self):
#         company_name = self.request.session.get("context")
#         queryset = CisDf.objects.filter(corp=company_name)
#         return queryset
