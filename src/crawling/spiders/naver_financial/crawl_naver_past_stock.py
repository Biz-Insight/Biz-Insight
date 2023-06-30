# 과거 주가 크롤링

from crawl_module import *
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

# crawl
#stock_price_df_per_month = crawl_stock_price(
#    df=import_df, start_time="20180101", end_time="20220630", time_frame="month")

stock_price_df_per_day = crawl_stock_price(df = import_df,
                                           start_time = last_year,
                                           end_time = today,
                                           time_frame = 'day')

# export data to sql
# export_to_mysql(df = corp_realtime_df,
#                username = 'multi',
#                password = 'Campus123!',
#                host_ip = '15-152-211-160',
#                database_name = 'raw_data',
#                desired_table_name ='corp_realtime_data')

# insert data to sql
#insert_to_mysql(
#    df=stock_price_df_per_month,
#    username="multi",
#    password="Campus123!",
#    host_ip="15-152-211-160",
#    database_name="stock_data",
#    desired_table_name="stock_data_per_month")

insert_to_mysql(df = stock_price_df_per_day,
                username = 'multi',
                password = 'Campus123!',
                host_ip = '15-152-211-160',
                database_name = 'stock_data',
                desired_table_name ='stock_data_per_day')
