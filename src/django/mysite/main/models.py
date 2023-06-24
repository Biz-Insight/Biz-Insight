from django.db import models


# Create your models here.
class Company(models.Model):
    Standard_code = models.CharField(max_length=20, verbose_name="표준코드", unique=True)
    Short_code = models.IntegerField(verbose_name="요약코드")
    Company_full_name = models.CharField(max_length=256, verbose_name="기업명")
    Company_name = models.CharField(max_length=256, verbose_name="기업약명")

    def __str__(self):
        return self.Company_name

    class Meta:
        # DataMart Table
        db_table = "company_name"
