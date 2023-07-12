import pymysql
import pandas as pd
import numpy as np
import warnings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

warnings.filterwarnings("ignore", category=FutureWarning)

username = "*****"
password = "*****"
hostname = "ec2-15-152-211-160.ap-northeast-3.compute.amazonaws.com"
database_name = "Data_Mart"
desired_table_name = "credit_analysis_features"

cnx = pymysql.connect(
    user=username,
    password=password,
    host=hostname,
    database=database_name,
)

query = "SELECT * FROM Data_Warehouse.final_features;"
final_features = pd.read_sql(query, cnx)

query = "SELECT * FROM Data_Warehouse.economic_indicators;"
economic_indicators = pd.read_sql(query, cnx)

query = "SELECT * FROM Data_Warehouse.credit_rank;"
credit_rank = pd.read_sql(query, cnx)

query = "SELECT * FROM Data_Warehouse.final_rating;"
final_rating = pd.read_sql(query, cnx)

cnx.close()

credit_analysis_features = final_features.merge(
    economic_indicators, how="left", on="year"
)

credit_rank_subset = credit_rank[["corp", "year", "total_rank", "simple_total_rank"]]
credit_analysis_features = credit_analysis_features.copy().merge(
    credit_rank_subset, how="left", on=["corp", "year"]
)

final_rating_subset = final_rating.drop("stock_code", axis=1)
credit_analysis_features = credit_analysis_features.copy().merge(
    final_rating_subset, how="left", on="corp"
)


credit_analysis_features = credit_analysis_features.rename(
    columns={
        "minimum_wag": "minimum_wage",
        "uskor_exchange_average": "us_kor_exchange_avg",
        "PPI_year": "ppi_year",
    }
)


cnx = pymysql.connect(user=username, password=password, host=hostname)
cursor = cnx.cursor()

engine = create_engine(
    "mysql+pymysql://{user}:{pw}@{host}/{db}".format(
        user=username, pw=password, db=database_name, host=hostname
    )
)
Session = sessionmaker(bind=engine)
session = Session()

try:
    credit_analysis_features.to_sql(
        desired_table_name, con=engine, if_exists="replace", index=False, chunksize=1000
    )
    session.commit()
except:
    session.rollback()
    raise
finally:
    session.close()

cursor.close()
cnx.close()
