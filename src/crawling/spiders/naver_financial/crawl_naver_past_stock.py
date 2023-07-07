# 과거 주가 크롤링
content = input(
    "월별 자료 수집 : 1, 일별 자료 수집 : 2 \
                :"
)

from naver_financial_crawl_module import (
    import_from_mysql,
    crawl_stock_price,
    insert_to_mysql,
    export_to_mysql,
)

from datetime import date

today = date.today().strftime("%Y%m%d")
last_year = str(int(today) - 10000)

# import data from sql
import_df = import_from_mysql(
    username="multi",
    password="Campus123!",
    host_ip="15-152-211-160",
    database_name="raw_data",
    desired_table_name="corp_list",
)


if content == 1:
    stock_price_df_per_month = crawl_stock_price(
        df=import_df, start_time="20180101", end_time=today, time_frame="month"
    )

    export_to_mysql(
        df=stock_price_df_per_month,
        username="multi",
        password="Campus123!",
        host_ip="15-152-211-160",
        database_name="stock_data",
        desired_table_name="stock_data_per_month",
    )

elif content == 2:
    stock_price_df_per_day = crawl_stock_price(
        df=import_df, start_time=last_year, end_time=today, time_frame="day"
    )

    export_to_mysql(
        df=stock_price_df_per_day,
        username="multi",
        password="Campus123!",
        host_ip="15-152-211-160",
        database_name="stock_data",
        desired_table_name="stock_data_per_month",
    )
