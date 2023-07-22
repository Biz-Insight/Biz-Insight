from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView
from .models import *
from django.http import JsonResponse
from django.views import View
import pandas as pd
import pickle
from math import floor
from .django_transform import django_transform
import json


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
    model = InvestmentData
    template_name = "financial_analysis.html"
    context_object_name = "financial_analysis"

    def get_queryset(self):
        company_name = self.request.session.get("context")
        queryset = InvestmentData.objects.filter(corp=company_name)
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
    model = CreditData
    template_name = "credit_indicator.html"
    context_object_name = "credit_indicator"

    def get_queryset(self):
        company_name = self.request.session.get("context")
        queryset = CreditData.objects.filter(corp=company_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        credit_indicator = context["credit_indicator"]

        # List of labels that need to be divided by 100,000,000
        labels_to_divide = [
            "자산총계",
            "부채총계",
            "자본총계",
            "총차입금",
            "순차입금",
            "유동부채금액",
            "운전자본",
            "당좌자산",
            "현금성자산",
            "단기성차입금",
            "매출액",
            "매출원가",
            "판매관리비",
            "EBIT",
            "자산총계",
            "영업활동현금흐름",
            "잉여현금흐름",
            "금융비용",
            "EBITDA",
            "법인세납부",
        ]

        # Update the values of the specified labels by dividing them by 100,000,000
        for data in credit_indicator:
            if data.label_ko in labels_to_divide:
                data.number_2018 /= 100000000
                data.number_2019 /= 100000000
                data.number_2020 /= 100000000
                data.number_2021 /= 100000000
                data.number_2022 /= 100000000

        desired_labels_stability = [
            "자산총계",
            "부채총계",
            "자본총계",
            "총차입금",
            "순차입금",
            "부채비율",
            "차입금의존도",
            "순차입금의존도",
            "총차입금/EBITDA",
            "순차입금/EBITDA",
            "EBITDA/금융비용",
            "영업활동현금흐름/총차입금",
            "총자산레버리지",
            "유동부채금액",
            "유동부채비율",
            "운전자본",
            "당좌자산",
        ]
        context["credit_indicator_stability"] = [
            data
            for data in credit_indicator
            if data.label_ko in desired_labels_stability
        ]

        desired_labels_liquidity = [
            "현금성자산",
            "단기성차입금",
            "현금성자산/단기성차입금",
            "단기성차입금/총차입금",
            "매출채권회전일수",
        ]
        context["credit_indicator_liquidity"] = [
            data
            for data in credit_indicator
            if data.label_ko in desired_labels_liquidity
        ]

        desired_labels_profitability = [
            "매출액",
            "매출원가",
            "판매관리비",
            "EBIT",
            "EBIT마진",
            "EBITDA/매출액",
            "자산총계",
            "총자산수익률()",
        ]
        context["credit_indicator_profitability"] = [
            data
            for data in credit_indicator
            if data.label_ko in desired_labels_profitability
        ]

        desired_labels_cash_flow = ["영업활동현금흐름", "잉여현금흐름", "금융비용", "EBITDA", "법인세납부"]
        context["credit_indicator_cash_flow"] = [
            data
            for data in credit_indicator
            if data.label_ko in desired_labels_cash_flow
        ]

        context["credit_indicator_stability"] = sorted(
            context["credit_indicator_stability"],
            key=lambda data: desired_labels_stability.index(data.label_ko),
        )

        context["credit_indicator_liquidity"] = sorted(
            context["credit_indicator_liquidity"],
            key=lambda data: desired_labels_liquidity.index(data.label_ko),
        )

        context["credit_indicator_profitability"] = sorted(
            context["credit_indicator_profitability"],
            key=lambda data: desired_labels_profitability.index(data.label_ko),
        )

        context["credit_indicator_cash_flow"] = sorted(
            context["credit_indicator_cash_flow"],
            key=lambda data: desired_labels_cash_flow.index(data.label_ko),
        )

        return context


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
    def get(self, request, chart_type, *args, **kwargs):
        company_name = request.GET.get("company_name", None)
        data = {}

        if company_name:
            if chart_type == "profitability_indicator":
                sales_data = Visualization.objects.filter(
                    corp=company_name, label_ko="매출액"
                )
                profit_margin_data = Visualization.objects.filter(
                    corp=company_name, label_ko="영업이익률"
                )
                net_profit_margin_data = Visualization.objects.filter(
                    corp=company_name, label_ko="순이익률"
                )

                data = {
                    "sales": list(
                        sales_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                    "profit_margin": list(
                        profit_margin_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                    "net_profit_margin": list(
                        net_profit_margin_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                }

            elif chart_type == "return_investment":
                roe_data = Visualization.objects.filter(
                    corp=company_name, label_ko="ROE"
                )
                roa_data = Visualization.objects.filter(
                    corp=company_name, label_ko="ROA"
                )
                roic_data = Visualization.objects.filter(
                    corp=company_name, label_ko="ROIC"
                )
                net_income_data = Visualization.objects.filter(
                    corp=company_name, label_ko="당기순이익"
                )

                data = {
                    "roe": list(
                        roe_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                    "roa": list(
                        roa_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                    "roic": list(
                        roic_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                    "net_income": list(
                        net_income_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                }

            elif chart_type == "profitability_growth":
                revenue_growth_data = Visualization.objects.filter(
                    corp=company_name, label_ko="매출액증가율"
                )
                operating_income_data = Visualization.objects.filter(
                    corp=company_name, label_ko="영업이익증가율"
                )
                net_income_data = Visualization.objects.filter(
                    corp=company_name, label_ko="순이익증가율"
                )

                data = {
                    "revenue_growth": list(
                        revenue_growth_data.values(
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                    "operating_income": list(
                        operating_income_data.values(
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                    "net_income": list(
                        net_income_data.values(
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                }

            elif chart_type == "asset_growth":
                asset_growth_data = Visualization.objects.filter(
                    corp=company_name, label_ko="총자산증가율"
                )
                tangible_asset_data = Visualization.objects.filter(
                    corp=company_name, label_ko="유형자산증가율"
                )
                total_equity_data = Visualization.objects.filter(
                    corp=company_name, label_ko="자기자본증가율"
                )

                data = {
                    "asset_growth": list(
                        asset_growth_data.values(
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                    "tangible_asset": list(
                        tangible_asset_data.values(
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                    "total_equity": list(
                        total_equity_data.values(
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                }
            elif chart_type == "stability":
                debt_data = Visualization.objects.filter(
                    corp=company_name, label_ko="부채비율"
                )
                current_liabilities_data = Visualization.objects.filter(
                    corp=company_name, label_ko="유동부채비율"
                )
                non_current_liabilities_data = Visualization.objects.filter(
                    corp=company_name, label_ko="비유동부채비율"
                )

                data = {
                    "debt": list(
                        debt_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                    "current_liabilities": list(
                        current_liabilities_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                    "non_current_liabilities": list(
                        non_current_liabilities_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                }

        if not data:
            return JsonResponse({"error": "Invalid parameters"}, status=400)

        return JsonResponse(data, safe=False)


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
    credit_prediction_json = request.session.get("credit_prediction")
    main_fs_json = request.session.get("main_fs")
    credit_data_web_json = request.session.get("credit_data_web")
    investment_data_web_json = request.session.get("investment_data_web")

    credit_prediction_dict = json.loads(credit_prediction_json)
    main_fs_dict = json.loads(main_fs_json)
    credit_data_web_dict = json.loads(credit_data_web_json)
    investment_data_web_dict = json.loads(investment_data_web_json)


    # credit_prediction_df = pd.DataFrame(credit_prediction_dict)
    # main_fs_df = pd.DataFrame(main_fs_dict)
    # credit_data_web_df = pd.DataFrame(credit_data_web_dict)
    # investment_data_web_df = pd.DataFrame(investment_data_web_dict)

    # bs_data = main_fs_df[main_fs_df["fs_type"] == "bs"]
    # incs_data = main_fs_df[main_fs_df["fs_type"] == "incs"]
    # cf_data = main_fs_df[main_fs_df["fs_type"] == "cf"]

    context = {
        "credit_prediction": credit_prediction_dict,
        "main_fs": main_fs_dict,
        "credit_data_web": credit_data_web_dict,
        "investment_data_web": investment_data_web_dict,
        # "bs_data": bs_data,
        # "incs_data": incs_data,
        # "cf_data": cf_data,
    }

    request.session["credit_prediction"] = credit_prediction_json
    request.session["main_fs"] = main_fs_json
    request.session["credit_data_web"] = credit_data_web_json
    request.session["investment_data_web"] = investment_data_web_json

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
