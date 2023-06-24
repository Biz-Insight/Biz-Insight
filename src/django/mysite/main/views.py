from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView
from .models import Company


def company_direct(request):
    return render(request, "company_list.html")


def search_view(request):
    company_name = request.GET.get("company_name", "")
    request.session["context"] = company_name
    return redirect("company_info")


def home(request):
    return render(request, "index.html")


class CompanyList(ListView):
    model = Company
    template_name = "company_list.html"
    context_object_name = "company_list"


class Companyinfo(ListView):
    model = Company
    template_name = "company_info.html"
    context_object_name = "company_info"

    def get_queryset(self):
        company_name = self.request.session.get("context")
        queryset = Company.objects.filter(Company_name=company_name)
        return queryset
