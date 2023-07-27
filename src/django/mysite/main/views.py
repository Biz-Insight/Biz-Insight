from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView
from .models import *
from django.http import JsonResponse
from django.views import View
import pandas as pd
import pickle
from math import floor
from .django_transform import django_transform
from .utils.openai_utils import get_corp_summary
from .utils.wordcloud_utils import *
import json
from .django_info import django_info


def home(request):
    return render(request, "index.html")


def company_direct(request):
    return render(request, "company_list.html")


def search_view(request):
    company_name = request.GET.get("company_name")
    request.session["context"] = company_name
    return redirect("company_info", company_name=company_name)


def get_gpt_summary_view(request):
    company_name = request.GET.get("company_name")
    summary = get_corp_summary(company_name)
    return JsonResponse({"summary": summary})


class CompanyList(ListView):
    model = CompanyInfo
    template_name = "company_list.html"
    context_object_name = "company_list"


class CompanyInfoWeb(ListView):
    model = CompanyInfo
    template_name = "company_info.html"
    context_object_name = "company_info"

    def get_queryset(self):
        company_name = self.request.session.get("context")
        queryset = CompanyInfo.objects.filter(corp=company_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_name = self.request.session.get("context")

        try:
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
        except Exception as e:
            print(f"Error occurred while fetching ratings: {e}")
            context["rating_data"] = None
            context["rating_stars"] = "별점을 불러오는데 실패했습니다."

        try:
            context["corp_summary"] = get_corp_summary(company_name)
        except Exception as e:
            print(f"Error occurred while fetching corp summary: {e}")
            context["corp_summary"] = "기업 정보 요약을 불러오는데 실패했습니다."

        stop_words = ["단점", "장점", "회사", "사람"]
        try:
            wordCloud(pre_df, stop_words, company_name, "up_pos")
            wordCloud(pre_df, stop_words, company_name, "down_pos")
            context[
                "wordcloud_image_up"
            ] = f"static/wordcloud_images/{company_name}_up_pos_wordcloud.png"
            context[
                "wordcloud_image_down"
            ] = f"static/wordcloud_images/{company_name}_down_pos_wordcloud.png"
        except Exception as e:
            print(f"Error occurred while generating wordcloud: {e}")
            context["wordcloud_image_up"] = "워드클라우드를 불러오는데 실패했습니다."
            context["wordcloud_image_down"] = "워드클라우드를 불러오는데 실패했습니다."

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
    model = CreditData
    template_name = "credit_analysis.html"
    context_object_name = "credit_analysis"

    def get_queryset(self):
        company_name = self.request.session.get("context")
        queryset = CreditData.objects.filter(corp=company_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_name = self.request.session.get("context")
        mainfs_data = MainFs.objects.filter(corp=company_name)
        company_credit = CreditData.objects.filter(corp=company_name).first()
        sector_name = company_credit.sector
        credit_indicator = context["credit_analysis"]
        company_info = CompanyInfo.objects.filter(corp=company_name).first()
        rank = company_info.rank
        predicted_rank = company_info.predicted_rank

        context["rank"] = rank
        context["predicted_rank"] = predicted_rank

        # 클래스 인스턴스
        revenue_temp = [data for data in credit_indicator if data.label_ko == "매출액"]

        revenue_2022 = revenue_temp[0].number_2022

        cluster_label, top_correlation, sector_credit_rating = django_info(
            revenue_2022, sector_name
        )

        sector_credit_rating_dict = sector_credit_rating.to_dict("records")
        top_correlation_dict = top_correlation.to_dict("records")

        context["cluster_label"] = cluster_label
        context["top_correlation"] = top_correlation_dict
        context["sector_credit_rating"] = sector_credit_rating_dict

        top_correlation_list = top_correlation["feature"].to_list()
        context["temp"] = top_correlation_list

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

        desired_labels = {
            "feature_importance": ["자산총계", "자본총계", "당좌자산", "시가총액", "매출액"],
            "summary": [
                "EBITDA마진",
                "EBITDA/금융비용",
                "부채비율",
                "순차입금의존도",
                "영업현금흐름/총차입금입금",
                "순차입금/EBITDA",
            ],
            "industry_correlation": top_correlation_list,
        }
        context["feature_importance"] = [
            data
            for data in credit_indicator
            if data.label_ko in desired_labels["feature_importance"]
        ]

        context["summary"] = [
            data
            for data in credit_indicator
            if data.label_ko in desired_labels["summary"]
        ]

        context["industry_correlation"] = [
            data
            for data in credit_indicator
            if data.label_en in desired_labels["industry_correlation"]
        ]

        context["feature_importance"] = sorted(
            context["feature_importance"],
            key=lambda data: desired_labels["feature_importance"].index(data.label_ko),
        )

        context["summary"] = sorted(
            context["summary"],
            key=lambda data: desired_labels["summary"].index(data.label_ko),
        )

        context["industry_correlation"] = sorted(
            context["industry_correlation"],
            key=lambda data: desired_labels["industry_correlation"].index(
                data.label_en
            ),
        )

        return context


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

            elif chart_type == "turnover":
                asset_data = Visualization.objects.filter(
                    corp=company_name, label_ko="총자산회전율"
                )
                accounts_receivable_data = Visualization.objects.filter(
                    corp=company_name, label_ko="매출채권회전율"
                )
                inventory_data = Visualization.objects.filter(
                    corp=company_name, label_ko="재고자산회전율"
                )
                accounts_payable_data = Visualization.objects.filter(
                    corp=company_name, label_ko="매입채무회전율"
                )
                data = {
                    "asset": list(
                        asset_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                    "accounts_receivable": list(
                        accounts_receivable_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                    "inventory": list(
                        inventory_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                    "accounts_payable": list(
                        accounts_payable_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                }
            elif chart_type == "per_share":
                eps_data = Visualization.objects.filter(
                    corp=company_name, label_ko="EPS"
                )
                bps_data = Visualization.objects.filter(
                    corp=company_name, label_ko="BPS"
                )

                data = {
                    "eps": list(
                        eps_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                    "bps": list(
                        bps_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                }
            elif chart_type == "value":
                per_data = Visualization.objects.filter(
                    corp=company_name, label_ko="PER"
                )
                pbr_data = Visualization.objects.filter(
                    corp=company_name, label_ko="PBR"
                )
                pcr_data = Visualization.objects.filter(
                    corp=company_name, label_ko="PCR"
                )

                data = {
                    "per": list(
                        per_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                    "pbr": list(
                        pbr_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                    "pcr": list(
                        pcr_data.values(
                            "number_2018",
                            "number_2019",
                            "number_2020",
                            "number_2021",
                            "number_2022",
                        )
                    ),
                }

            elif chart_type == "industry":
                company_investment = CompanyInvestment.objects.filter(
                    corp=company_name
                ).first()
                sector_name = company_investment.sector
                data["company"] = {
                    "profitability": company_investment.profitability,
                    "growth": company_investment.growth,
                    "stability": company_investment.stability,
                    "activity": company_investment.activity,
                    "valuation": company_investment.valuation,
                }

                industry_investment = IndustryInvestment.objects.filter(
                    sector=sector_name
                ).first()
                data["industry"] = {
                    "profitability": industry_investment.profitability,
                    "growth": industry_investment.growth,
                    "stability": industry_investment.stability,
                    "activity": industry_investment.activity,
                    "valuation": industry_investment.valuation,
                }
                data["sector_name"] = sector_name
                data["company_name"] = company_name

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
            credit_group_prediction,
            main_fs,
            credit_data_web,
            investment_data_web,
            top_correlation,
            sector_credit_rating,
        ) = django_transform(csv_file)

        request.session["credit_group_prediction"] = credit_group_prediction
        request.session["main_fs"] = main_fs.to_json(orient="columns")
        request.session["credit_data_web"] = credit_data_web.to_json(orient="columns")
        request.session["investment_data_web"] = investment_data_web.to_json(
            orient="columns"
        )
        request.session["top_correlation"] = top_correlation.to_json(orient="columns")
        request.session["sector_credit_rating"] = sector_credit_rating.to_json(
            orient="columns"
        )

        return redirect("new_credit_analysis")
    return render(request, "credit_request.html")


def new_credit_analysis(request):
    # 현재 json 자료형
    credit_group_prediction = request.session["credit_group_prediction"]
    main_fs_json = request.session["main_fs"]
    credit_data_web_json = request.session["credit_data_web"]
    investment_data_web_json = request.session["investment_data_web"]
    top_correlation_json = request.session["top_correlation"]
    sector_credit_rating_json = request.session["sector_credit_rating"]

    # 새션 재 전송
    request.session["credit_group_prediction"] = credit_group_prediction
    request.session["main_fs"] = main_fs_json
    request.session["credit_data_web"] = credit_data_web_json
    request.session["investment_data_web"] = investment_data_web_json
    request.session["top_correlation"] = top_correlation_json
    request.session["sector_credit_rating"] = sector_credit_rating_json

    # pandas df로 불러오기
    main_fs_df = pd.read_json(main_fs_json, orient="columns")
    credit_data_web_df = pd.read_json(credit_data_web_json, orient="columns")
    investment_data_web_df = pd.read_json(investment_data_web_json, orient="columns")
    top_correlation_df = pd.read_json(top_correlation_json, orient="columns")
    sector_credit_rating_df = pd.read_json(sector_credit_rating_json, orient="columns")

    desired_labels = {
        "feature_importance": ["자산총계", "자본총계", "당좌자산", "시가총액", "매출액"],
        "summary": [
            "EBITDA마진",
            "EBITDA/금융비용",
            "부채비율",
            "순차입금의존도",
            "영업현금흐름/총차입금입금",
            "순차입금/EBITDA",
        ],
        "industry_correlation": [
            "매출액",
            "매출원가",
            "판매관리비",
            "EBIT",
            "EBIT마진",
            "EBITDA/매출액",
            "자산총계",
            "총자산수익률()",
        ],
    }

    feature_importance_credit_data_web_df = credit_data_web_df[
        credit_data_web_df["label_ko"].isin(desired_labels["feature_importance"])
    ]

    feature_importance_main_fs_df = main_fs_df[
        main_fs_df["label_ko"].isin(desired_labels["feature_importance"])
    ]
    feature_importance_main_fs_df = feature_importance_main_fs_df.drop(
        columns=["fs_type"]
    )

    feature_importance_credit_data_web_df.reset_index(drop=True, inplace=True)
    feature_importance_main_fs_df.reset_index(drop=True, inplace=True)

    # 컬럼 순서 정의
    columns_order = [
        "corp",
        "sector",
        "label_en",
        "label_ko",
        "current_year",
        "industry_avg",
        "cluster_max",
        "cluster_median",
        "cluster_min",
    ]

    # 각 데이터프레임의 컬럼 순서를 조정
    feature_importance_credit_data_web_df = feature_importance_credit_data_web_df[
        columns_order
    ]
    feature_importance_main_fs_df = feature_importance_main_fs_df[columns_order]

    # 두 데이터프레임을 행 방향으로 결합
    feature_importance = pd.concat(
        [feature_importance_credit_data_web_df, feature_importance_main_fs_df],
        axis=0,
        ignore_index=True,
    )

    summary = credit_data_web_df[
        credit_data_web_df["label_ko"].isin(desired_labels["summary"])
    ]

    industry_correlation = credit_data_web_df[
        credit_data_web_df["label_ko"].isin(desired_labels["industry_correlation"])
    ]

    # 데이터프레임을 사전 형태로 변환
    # 데이터프레임을 사전 형태로 변환하고 JSON 문자열로 변환
    main_fs = main_fs_df.to_dict("records")
    credit_data_web = credit_data_web_df.to_dict("records")
    investment_data_web = investment_data_web_df.to_dict("records")
    top_correlation = top_correlation_df.to_dict("records")
    sector_credit_rating = sector_credit_rating_df.to_dict("records")
    feature_importance = feature_importance.to_dict("records")
    summary = summary.to_dict("records")
    industry_correlation = industry_correlation.to_dict("records")

    context = {
        "credit_group_prediction": credit_group_prediction,
        "main_fs": main_fs,
        "credit_data_web": credit_data_web,
        "investment_data_web": investment_data_web,
        "top_correlation": top_correlation,
        "sector_credit_rating": sector_credit_rating,
        "feature_importance": feature_importance,
        "summary": summary,
        "industry_correlation": industry_correlation,
    }

    return render(request, "new_credit_analysis.html", context)


def new_financial_statements(request):
    # 현재 json 자료형
    credit_group_prediction = request.session["credit_group_prediction"]
    main_fs_json = request.session["main_fs"]
    credit_data_web_json = request.session["credit_data_web"]
    investment_data_web_json = request.session["investment_data_web"]
    top_correlation_json = request.session["top_correlation"]
    sector_credit_rating_json = request.session["sector_credit_rating"]

    # 새션 재 전송
    request.session["credit_group_prediction"] = credit_group_prediction
    request.session["main_fs"] = main_fs_json
    request.session["credit_data_web"] = credit_data_web_json
    request.session["investment_data_web"] = investment_data_web_json
    request.session["top_correlation"] = top_correlation_json
    request.session["sector_credit_rating"] = sector_credit_rating_json

    main_fs_df = pd.read_json(main_fs_json, orient="columns")

    bs = main_fs_df[main_fs_df["fs_type"] == "bs"]
    incs = main_fs_df[main_fs_df["fs_type"] == "incs"]
    cf = main_fs_df[main_fs_df["fs_type"] == "cf"]

    bs_dict = bs.to_dict("records")
    incs_dict = incs.to_dict("records")
    cf_dict = cf.to_dict("records")

    context = {"bs": bs_dict, "incs": incs_dict, "cf": cf_dict}

    return render(request, "new_financial_statements.html", context)


def new_financial_analysis(request):
    credit_prediction = request.session.get("credit_prediction")
    main_fs_json = request.session.get("main_fs")
    credit_data_web_json = request.session.get("credit_data_web")
    investment_data_web_json = request.session.get("investment_data_web")

    main_fs_dict = json.loads(main_fs_json)
    credit_data_web_dict = json.loads(credit_data_web_json)
    investment_data_web_dict = json.loads(investment_data_web_json)

    context = {
        "credit_prediction": credit_prediction,
        "main_fs": main_fs_dict,
        "credit_data_web": credit_data_web_dict,
        "investment_data_web": investment_data_web_dict,
    }

    request.session["credit_prediction"] = credit_prediction
    request.session["main_fs"] = main_fs_json
    request.session["credit_data_web"] = credit_data_web_json
    request.session["investment_data_web"] = investment_data_web_json

    return render(request, "new_financial_analysis.html", context)


def new_credit_indicator(request):
    # 현재 json 자료형
    credit_group_prediction = request.session["credit_group_prediction"]
    main_fs_json = request.session["main_fs"]
    credit_data_web_json = request.session["credit_data_web"]
    investment_data_web_json = request.session["investment_data_web"]
    top_correlation_json = request.session["top_correlation"]
    sector_credit_rating_json = request.session["sector_credit_rating"]

    # 새션 재 전송
    request.session["credit_group_prediction"] = credit_group_prediction
    request.session["main_fs"] = main_fs_json
    request.session["credit_data_web"] = credit_data_web_json
    request.session["investment_data_web"] = investment_data_web_json
    request.session["top_correlation"] = top_correlation_json
    request.session["sector_credit_rating"] = sector_credit_rating_json

    # pandas df로 불러오기
    credit_data_web_df = pd.read_json(credit_data_web_json, orient="columns")
    main_fs_df = pd.read_json(main_fs_json, orient="columns")

    desired_labels = {
        "stability": [
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
        ],
        "liquidity": [
            "현금성자산",
            "단기성차입금",
            "현금성자산/단기성차입금",
            "단기성차입금/총차입금",
            "매출채권회전일수",
        ],
        "profitability": [
            "매출액",
            "매출원가",
            "판매관리비",
            "EBIT",
            "EBIT마진",
            "EBITDA/매출액",
            "자산총계",
            "총자산수익률()",
        ],
        "cash_flow": [
            "영업활동현금흐름",
            "잉여현금흐름",
            "금융비용",
            "EBITDA",
            "법인세납부",
        ],
    }

    stability_df = credit_data_web_df[
        credit_data_web_df["label_ko"].isin(desired_labels["stability"])
    ]

    liquidity_df = credit_data_web_df[
        credit_data_web_df["label_ko"].isin(desired_labels["liquidity"])
    ]

    profitability_df = credit_data_web_df[
        credit_data_web_df["label_ko"].isin(desired_labels["profitability"])
    ]

    cash_flow_df = credit_data_web_df[
        credit_data_web_df["label_ko"].isin(desired_labels["cash_flow"])
    ]
    stability_web = stability_df.to_dict("records")
    liquidity_web = liquidity_df.to_dict("records")
    profitability_web = profitability_df.to_dict("records")
    cash_flow_web = cash_flow_df.to_dict("records")

    context = {
        "stability": stability_web,
        "liquidity": liquidity_web,
        "profitability": profitability_web,
        "cash_flow": cash_flow_web,
    }

    return render(request, "new_credit_indicator.html", context)


def new_investment_indicator(request):
    # 현재 json 자료형
    credit_group_prediction = request.session["credit_group_prediction"]
    main_fs_json = request.session["main_fs"]
    credit_data_web_json = request.session["credit_data_web"]
    investment_data_web_json = request.session["investment_data_web"]
    top_correlation_json = request.session["top_correlation"]
    sector_credit_rating_json = request.session["sector_credit_rating"]

    # 새션 재 전송
    request.session["credit_group_prediction"] = credit_group_prediction
    request.session["main_fs"] = main_fs_json
    request.session["credit_data_web"] = credit_data_web_json
    request.session["investment_data_web"] = investment_data_web_json
    request.session["top_correlation"] = top_correlation_json
    request.session["sector_credit_rating"] = sector_credit_rating_json

    # pandas df로 불러오기
    credit_data_web_df = pd.read_json(credit_data_web_json, orient="columns")
    investment_data_web_df = pd.read_json(investment_data_web_json, orient="columns")

    desired_labels = {
        "profitability": [
            "매출총이익률",
            "영업이익률",
            "순이익률",
            "EBITDA마진율",
            "ROE",
            "ROA",
            "ROIC",
        ],
        "stability": [
            "부채비율",
            "유동비율",
            "당좌비율",
            "비유동부채비율",
            "자기자본비율",
            "이자보상배율",
            "차입금비율",
            "순부채비율",
            "자본유보율",
        ],
        "activity": [
            "총자산회전율",
            "자기자본회전율",
            "순운전자본회전율",
            "유형자산회전율",
            "매출채권회전율",
            "재고자산회전율",
            "매입채무회전율",
        ],
        "valuation": ["EPS", "BPS", "PER", "PBR", "PCR", "EV/EBITDA"],
    }

    profitability_df = investment_data_web_df[
        investment_data_web_df["label_ko"].isin(desired_labels["profitability"])
    ]

    stability_df = investment_data_web_df[
        investment_data_web_df["label_ko"].isin(desired_labels["stability"])
    ]

    activity_df = investment_data_web_df[
        investment_data_web_df["label_ko"].isin(desired_labels["activity"])
    ]

    valuation_df = investment_data_web_df[
        investment_data_web_df["label_ko"].isin(desired_labels["valuation"])
    ]
    credit_data_web = credit_data_web_df.to_dict("records")
    investment_data_web = investment_data_web_df.to_dict("records")
    profitability = profitability_df.to_dict("records")
    stability = stability_df.to_dict("records")
    activity = activity_df.to_dict("records")
    valuation = valuation_df.to_dict("records")

    context = {
        "credit_data_web": credit_data_web,
        "investment_data_web": investment_data_web,
        "investment_indicator_profitability": profitability,
        "investment_indicator_stability": stability,
        "investment_indicator_activity": activity,
        "investment_indicator_valuation": valuation,
    }

    return render(request, "new_investment_indicator.html", context)
