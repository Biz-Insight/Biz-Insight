# Generated by Django 2.1.7 on 2023-07-25 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_industryaverage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corp', models.TextField(blank=True, null=True)),
                ('stock_code', models.TextField(blank=True, null=True)),
                ('sector', models.TextField(blank=True, null=True)),
                ('main_product', models.TextField(blank=True, null=True)),
                ('listing_date', models.DateField(blank=True, null=True)),
                ('settlement_month', models.TextField(blank=True, null=True)),
                ('representative_name', models.TextField(blank=True, null=True)),
                ('homepage', models.TextField(blank=True, null=True)),
                ('region', models.TextField(blank=True, null=True)),
                ('rank', models.TextField(blank=True, null=True)),
                ('predicted_rank', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'company_info',
            },
        ),
    ]