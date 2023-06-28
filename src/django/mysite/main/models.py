from django.db import models


class CisDf(models.Model):
    corp = models.TextField(blank=True, null=True)
    account = models.TextField(blank=True, null=True)
    account_detail = models.TextField(blank=True, null=True)
    account_detail_2 = models.TextField(blank=True, null=True)
    number_2018 = models.FloatField(db_column="2018", blank=True, null=True)
    number_2019 = models.FloatField(db_column="2019", blank=True, null=True)
    number_2020 = models.FloatField(db_column="2020", blank=True, null=True)
    number_2021 = models.FloatField(db_column="2021", blank=True, null=True)
    number_2022 = models.FloatField(db_column="2022", blank=True, null=True)

    class Meta:
        db_table = "cis_df"


class CompanyName(models.Model):
    standard_code = models.CharField(
        db_column="Standard_code", unique=True, max_length=20
    )
    short_code = models.TextField(db_column="Short_code", blank=True, null=True)
    company_full_name = models.TextField(
        db_column="Company_full_name", blank=True, null=True
    )
    company_name = models.TextField(db_column="Company_name", blank=True, null=True)

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = "company_name"
