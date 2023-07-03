# CRB index 크롤링

from bok_crawl_module import insert_to_mysql, crawl_crb_data

# crawl crb data
crb_df = crawl_crb_data(from_year=2017)

# insert to MySQL
insert_to_mysql(
    df=crb_df,
    username="multi",
    password="Campus123!",
    host_ip="15-152-211-160",
    database_name="stock_data",
    desired_table_name="crb_index",
)
