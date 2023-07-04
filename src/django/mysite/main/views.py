from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView
from .models import CompanyName, CisDf, StockDay
from django.http import JsonResponse
from django.views import View


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


class CompanyNews(ListView):
    model = CompanyName
    template_name = "company_news.html"
    context_object_name = "company_news"

    def get_queryset(self):
        company_name = self.request.session.get("context")
        queryset = CompanyName.objects.filter(company_name=company_name)
        return queryset


class FinancialAnalysis(ListView):
    model = CompanyName
    template_name = "financial_analysis.html"
    context_object_name = "financial_analysis"

    def get_queryset(self):
        company_name = self.request.session.get("context")
        queryset = CompanyName.objects.filter(company_name=company_name)
        return queryset


class CreditAnalysis(ListView):
    model = CompanyName
    template_name = "credit_analysis.html"
    context_object_name = "credit_analysis"

    def get_queryset(self):
        company_name = self.request.session.get("context")
        queryset = CompanyName.objects.filter(company_name=company_name)
        return queryset


class FinancialStatements(ListView):
    model = CompanyName
    template_name = "financial_statements.html"
    context_object_name = "financial_statements"

    def get_queryset(self):
        company_name = self.request.session.get("context")
        queryset = CompanyName.objects.filter(company_name=company_name)
        return queryset


class InvestmentIndicator(ListView):
    model = CompanyName
    template_name = "investment_indicator.html"
    context_object_name = "investment_indicator"

    def get_queryset(self):
        company_name = self.request.session.get("context")
        queryset = CompanyName.objects.filter(company_name=company_name)
        return queryset


class CreditIndicator(ListView):
    model = CompanyName
    template_name = "credit_indicator.html"
    context_object_name = "credit_indicator"

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


class ChartData(View):
    def get(self, request, *args, **kwargs):
        company_name = request.GET.get("company_name", None)

        if company_name is not None:
            cis_df = CisDf.objects.filter(corp=company_name, account="매출원가")
            data = list(
                cis_df.values(
                    "number_2018",
                    "number_2019",
                    "number_2020",
                    "number_2021",
                    "number_2022",
                )
            )
            return JsonResponse(data, safe=False)

        else:
            return JsonResponse({"error": "Invalid parameters"}, status=400)


class StockArea(View):
    def get(self, request, *args, **kwargs):
        company_name = request.GET.get("company_name", None)

        if company_name is not None:
            stock_data = StockDay.objects.filter(corp=company_name).order_by("date")
            data = [day.close_price for day in stock_data]
            labels = [day.date.strftime("%Y-%m-%d") for day in stock_data]
            return JsonResponse({"data": data, "labels": labels})

        else:
            return JsonResponse({"error": "Invalid parameters"}, status=400)


# class CisDf(ListView):
#     model = CisDf
#     template_name = "company_info.html"
#     context_object_name = "cis_df"

#     def get_queryset(self):
#         company_name = self.request.session.get("context")
#         queryset = CisDf.objects.filter(corp=company_name)
#         return queryset
