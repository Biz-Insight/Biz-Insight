# 실시간 주가 및 주가 기반 투자지표 크롤링

from crawl_module import *
from datetime import date

today = date.today()

# import data from sql
import_df = import_from_mysql(
    username="multi",
    password="Campus123!",
    host_ip="15-152-211-160",
    database_name="raw_data",
    desired_table_name="corp_list",
)

# crawl
corp_realtime_df = crawl_realtime_data(df=import_df, today=today)

# export data to sql
# export_to_mysql(df = corp_realtime_df,
#                username = 'multi',
#                password = 'Campus123!',
#                host_ip = '15-152-211-160',
#                database_name = 'raw_data',
#                desired_table_name ='corp_realtime_data')

# insert data to sql
insert_to_mysql(
    df=corp_realtime_df,
    username="multi",
    password="Campus123!",
    host_ip="15-152-211-160",
    database_name="raw_data",
    desired_table_name="corp_realtime_data",
)
