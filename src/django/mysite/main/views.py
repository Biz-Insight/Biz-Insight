from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView
from .models import *
from django.http import JsonResponse
from django.views import View
import pandas as pd
import pickle
from math import floor
from .django_transform import django_transform


def home(request):
    return render(request, "index.html")


def company_direct(request):
    return render(request, "company_list.html")


def search_view(request):
    company_name = request.GET.get("company_name")
    request.session["context"] = company_name
    return redirect("company_info", company_name=company_name)


class CompanyList(ListView):
    model = CompanyName
    template_name = "company_list.html"
    context_object_name = "company_list"


from math import floor


class CompanyInfo(ListView):
    model = KospiCompanyInfo
    template_name = "company_info.html"
    context_object_name = "company_info"

    def get_queryset(self):
        company_name = self.request.session.get("context")
        queryset = KospiCompanyInfo.objects.filter(corp=company_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_name = self.request.session.get("context")
        rating_data = Rating.objects.filter(corp=company_name).first()
        context["rating_data"] = rating_data
        context["rating_stars"] = {
            "rating": self.get_rating_stars(rating_data, "rating"),
            "paywellfare": self.get_rating_stars(rating_data, "paywellfare"),
            "worklifebal": self.get_rating_stars(rating_data, "worklifebal"),
            "culture": self.get_rating_stars(rating_data, "culture"),
            "opportunity": self.get_rating_stars(rating_data, "opportunity"),
            "manager": self.get_rating_stars(rating_data, "manager"),
            "recommend": self.get_rating_stars(rating_data, "recommend"),
            "ceo": self.get_rating_stars(rating_data, "ceo"),
            "potential": self.get_rating_stars(rating_data, "potential"),
        }
        return context

    def get_rating_stars(self, rating_data, field):
        rating = getattr(rating_data, field)
        full_stars = floor(rating)
        half_star = False
        if 0.75 >= rating - full_stars >= 0.25:
            half_star = True
        elif rating - full_stars >= 0.75:
            full_stars = full_stars + 1
        empty_stars = 5 - full_stars - half_star
        return {
            "full_stars": range(full_stars),
            "half_star": half_star,
            "empty_stars": range(empty_stars),
        }


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
    model = MockupData
    template_name = "credit_analysis.html"
    context_object_name = "credit_analysis"

    def get_queryset(self):
        company_name = self.request.session.get("context")
        queryset = MockupData.objects.filter(corp=company_name)
        data_list = list(queryset.values())
        test_data = pd.DataFrame(data_list)
        model_data = test_data.drop(
            ["id", "ebit", "stock_code", "year", "sector", "corp"], axis=1
        )
        credit_model = pickle.load(open("static/test_model.pkl", "rb"))
        pred = credit_model.predict(model_data)
        context = {
            "company_name": test_data.corp,
            "year": test_data.year,
            "pred_result": pred,
        }
        context_df = pd.DataFrame(context)
        return context_df[:1]


class MainFinancialStatements(ListView):
    model = MainFs
    template_name = "financial_statements.html"
    context_object_name = "financial_statements"

    def get_queryset(self):
        company_name = self.request.session.get("context")
        queryset = MainFs.objects.filter(corp=company_name)
        return queryset


class InvestmentIndicator(ListView):
    model = InvestmentData
    template_name = "investment_indicator.html"
    context_object_name = "investment_indicator"

    def get_queryset(self):
        company_name = self.request.session.get("context")
        queryset = InvestmentData.objects.filter(corp=company_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        investment_indicator = context["investment_indicator"]
        desired_labels_profitability = [
            "매출총이익률",
            "영업이익률",
            "순이익률",
            "EBITDA마진율",
            "ROE",
            "ROA",
            "ROIC",
        ]
        context["investment_indicator_profitability"] = [
            data
            for data in investment_indicator
            if data.label_ko in desired_labels_profitability
        ]

        desired_labels_growth = [
            "매출액증가율",
            "영업이익증가율",
            "순이익증가율",
            "총자산증가율",
            "유형자산증가율",
            "부채총계증가율",
            "자기자본증가율",
        ]
        context["investment_indicator_growth"] = [
            data
            for data in investment_indicator
            if data.label_ko in desired_labels_growth
        ]

        desired_labels_stability = [
            "부채비율",
            "유동비율",
            "당좌비율",
            "비유동부채비율",
            "자기자본비율",
            "이자보상배율",
            "차입금비율",
            "순부채비율",
            "자본유보율",
        ]
        context["investment_indicator_stability"] = [
            data
            for data in investment_indicator
            if data.label_ko in desired_labels_stability
        ]

        desired_labels_activity = [
            "총자산회전율",
            "자기자본회전율",
            "순운전자본회전율",
            "유형자산회전율",
            "매출채권회전율",
            "재고자산회전율",
            "매입채무회전율",
        ]
        context["investment_indicator_activity"] = [
            data
            for data in investment_indicator
            if data.label_ko in desired_labels_activity
        ]

        desired_labels_valuation = ["EPS", "BPS", "PER", "PBR", "PCR", "EV/EBITDA"]
        context["investment_indicator_valuation"] = [
            data
            for data in investment_indicator
            if data.label_ko in desired_labels_valuation
        ]

        context["investment_indicator_profitability"] = sorted(
            context["investment_indicator_profitability"],
            key=lambda data: desired_labels_profitability.index(data.label_ko),
        )

        context["investment_indicator_growth"] = sorted(
            context["investment_indicator_growth"],
            key=lambda data: desired_labels_growth.index(data.label_ko),
        )

        context["investment_indicator_stability"] = sorted(
            context["investment_indicator_stability"],
            key=lambda data: desired_labels_stability.index(data.label_ko),
        )

        context["investment_indicator_activity"] = sorted(
            context["investment_indicator_activity"],
            key=lambda data: desired_labels_activity.index(data.label_ko),
        )

        context["investment_indicator_valuation"] = sorted(
            context["investment_indicator_valuation"],
            key=lambda data: desired_labels_valuation.index(data.label_ko),
        )

        return context


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


def search_view(request):
    company_name = request.GET.get("company_name")
    request.session["context"] = company_name
    return redirect("company_info", company_name=company_name)


def credit_request(request):
    if request.method == "POST":
        csv_file = request.FILES["file"]
        (
            credit_prediction,
            main_fs,
            credit_data_web,
            investment_data_web,
        ) = django_transform(csv_file)
        request.session["credit_prediction"] = main_fs.to_json(orient="split")
        request.session["main_fs"] = main_fs.to_json(orient="split")
        request.session["credit_data_web"] = main_fs.to_json(orient="split")
        request.session["investment_data_web"] = main_fs.to_json(orient="split")

        context = {
            "message": "파일이 성공적으로 처리되었습니다.",
            "credit_prediction": credit_prediction,
            "main_fs": main_fs,
            "credit_data_web": credit_data_web,
            "investment_data_web": investment_data_web,
        }
        return render(request, "csv_upload_result.html", context)
    return render(request, "credit_request.html")


def show_result(request):
    context = {"message": "파일이 성공적으로 처리되었습니다."}
    return render(request, "csv_upload_result.html")


def new_company_info(request):
    credit_prediction = request.session.get("credit_prediction")
    main_fs = request.session.get("main_fs")
    credit_data_web = request.session.get("credit_data_web")
    investment_data_web = request.session.get("investment_data_web")
    context = {
        "credit_prediction": credit_prediction,
        "main_fs": main_fs,
        "credit_data_web": credit_data_web,
        "investment_data_web": investment_data_web,
    }
    request.session["credit_prediction"] = credit_prediction
    request.session["main_fs"] = main_fs
    request.session["credit_data_web"] = credit_data_web
    request.session["investment_data_web"] = investment_data_web
    return render(request, "new_company_info.html", context)


def new_company_news(request):
    credit_prediction = request.session.get("credit_prediction")
    main_fs = request.session.get("main_fs")
    credit_data_web = request.session.get("credit_data_web")
    investment_data_web = request.session.get("investment_data_web")
    context = {
        "credit_prediction": credit_prediction,
        "main_fs": main_fs,
        "credit_data_web": credit_data_web,
        "investment_data_web": investment_data_web,
    }
    request.session["credit_prediction"] = credit_prediction
    request.session["main_fs"] = main_fs
    request.session["credit_data_web"] = credit_data_web
    request.session["investment_data_web"] = investment_data_web
    return render(request, "new_company_news.html", context)


def new_credit_analysis(request):
    credit_prediction = request.session.get("credit_prediction")
    main_fs = request.session.get("main_fs")
    credit_data_web = request.session.get("credit_data_web")
    investment_data_web = request.session.get("investment_data_web")
    context = {
        "credit_prediction": credit_prediction,
        "main_fs": main_fs,
        "credit_data_web": credit_data_web,
        "investment_data_web": investment_data_web,
    }
    request.session["credit_prediction"] = credit_prediction
    request.session["main_fs"] = main_fs
    request.session["credit_data_web"] = credit_data_web
    request.session["investment_data_web"] = investment_data_web
    return render(request, "new_credit_analysis.html", context)


def new_credit_indicator(request):
    credit_prediction = request.session.get("credit_prediction")
    main_fs = request.session.get("main_fs")
    credit_data_web = request.session.get("credit_data_web")
    investment_data_web = request.session.get("investment_data_web")
    context = {
        "credit_prediction": credit_prediction,
        "main_fs": main_fs,
        "credit_data_web": credit_data_web,
        "investment_data_web": investment_data_web,
    }
    request.session["credit_prediction"] = credit_prediction
    request.session["main_fs"] = main_fs
    request.session["credit_data_web"] = credit_data_web
    request.session["investment_data_web"] = investment_data_web
    return render(request, "new_credit_indicator.html", context)


def new_financial_analysis(request):
    credit_prediction = request.session.get("credit_prediction")
    main_fs = request.session.get("main_fs")
    credit_data_web = request.session.get("credit_data_web")
    investment_data_web = request.session.get("investment_data_web")
    context = {
        "credit_prediction": credit_prediction,
        "main_fs": main_fs,
        "credit_data_web": credit_data_web,
        "investment_data_web": investment_data_web,
    }
    request.session["credit_prediction"] = credit_prediction
    request.session["main_fs"] = main_fs
    request.session["credit_data_web"] = credit_data_web
    request.session["investment_data_web"] = investment_data_web
    return render(request, "new_financial_analysis.html", context)


def new_financial_statements(request):
    credit_prediction = request.session.get("credit_prediction")
    main_fs = request.session.get("main_fs")
    credit_data_web = request.session.get("credit_data_web")
    investment_data_web = request.session.get("investment_data_web")
    context = {
        "credit_prediction": credit_prediction,
        "main_fs": main_fs,
        "credit_data_web": credit_data_web,
        "investment_data_web": investment_data_web,
    }
    request.session["credit_prediction"] = credit_prediction
    request.session["main_fs"] = main_fs
    request.session["credit_data_web"] = credit_data_web
    request.session["investment_data_web"] = investment_data_web
    return render(request, "new_financial_statements.html", context)


def new_investment_indicator(request):
    credit_prediction = request.session.get("credit_prediction")
    main_fs = request.session.get("main_fs")
    credit_data_web = request.session.get("credit_data_web")
    investment_data_web = request.session.get("investment_data_web")
    context = {
        "credit_prediction": credit_prediction,
        "main_fs": main_fs,
        "credit_data_web": credit_data_web,
        "investment_data_web": investment_data_web,
    }
    request.session["credit_prediction"] = credit_prediction
    request.session["main_fs"] = main_fs
    request.session["credit_data_web"] = credit_data_web
    request.session["investment_data_web"] = investment_data_web
    return render(request, "new_investment_indicator.html", context)
