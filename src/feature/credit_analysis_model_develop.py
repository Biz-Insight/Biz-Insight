import pymysql
import pandas as pd
import warnings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

warnings.filterwarnings("ignore", category=FutureWarning)

username = "multi"
password = "*****!"
hostname = "ec2-15-152-211-160.ap-northeast-3.compute.amazonaws.com"
database_name = "Data_Mart"

cnx = pymysql.connect(
    user=username,
    password=password,
    host=hostname,
    database=database_name,
)


query = "SELECT * FROM Data_Warehouse.credit_data_model"
credit_data = pd.read_sql(query, cnx)

query = "SELECT * FROM Data_Warehouse.economic_indicators;"
economic_indicators = pd.read_sql(query, cnx)

query = "SELECT * FROM Data_Warehouse.credit_rank;"
credit_rank = pd.read_sql(query, cnx)

query = "SELECT * FROM Data_Warehouse.rating_filled;"
rating_filled = pd.read_sql(query, cnx)

query = "SELECT * FROM Data_Lake.crb_index;"
crb_index = pd.read_sql(query, cnx)

query = "SELECT * FROM Data_Warehouse.investment_data_model"
investment_data = pd.read_sql(query, cnx)

cnx.close()

avg_crb_index = crb_index.copy().groupby("year")["crb_index"].mean().reset_index()
avg_crb_index.columns = ["year", "crb_index_avg"]
avg_crb_index["year"] = avg_crb_index["year"].astype(int).astype(str)

credit_analysis_features = credit_data.merge(economic_indicators, how="left", on="year")

credit_rank_subset = credit_rank[["corp", "year", "rank"]]
credit_analysis_features = credit_analysis_features.copy().merge(
    credit_rank_subset, how="left", on=["corp", "year"]
)

rating_filled_subset = rating_filled.drop(["stock_code", "sector"], axis=1)
credit_analysis_features = credit_analysis_features.copy().merge(
    rating_filled_subset, how="left", on="corp"
)

credit_analysis_features = credit_analysis_features.merge(
    avg_crb_index, how="left", on="year"
)

credit_analysis_model_a = credit_analysis_features.copy()

current_features = set(credit_analysis_features.columns)
investment_features = set(investment_data.columns)
common_features = list(investment_features & current_features)

common_features.remove("corp")
common_features.remove("year")
common_features.remove("sector")
common_features.remove("stock_code")

investment_data = investment_data.drop(common_features, axis=1)

credit_analysis_features = credit_analysis_features.merge(
    investment_data, how="left", on=["corp", "year", "stock_code", "sector"]
)

credit_analysis_model_b = credit_analysis_features.copy()

for model in [credit_analysis_model_a, credit_analysis_model_b]:
    model.rename(
        columns={
            "minimum_wag": "minimum_wage",
            "uskor_exchange_average": "us_kor_exchange_avg",
            "PPI_year": "ppi_year",
        },
        inplace=True,
    )


credit_analysis_model_a.to_csv(
    "credit_analysis_model_a.csv", encoding="utf-8-sig", index=False
)
credit_analysis_model_b.to_csv(
    "credit_analysis_model_b.csv", encoding="utf-8-sig", index=False
)

data_tables = {
    "credit_analysis_model_a": credit_analysis_model_a,
    "credit_analysis_model_b": credit_analysis_model_b,
}

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{hostname}/{database_name}"
)
Session = sessionmaker(bind=engine)

for table_name, df in data_tables.items():
    try:
        with engine.begin() as connection, Session() as session:
            df.to_sql(
                table_name,
                con=connection,
                if_exists="replace",
                index=False,
                chunksize=1000,
            )
            session.commit()
    except Exception as e:
        print(f"An error occurred while processing {table_name}: {str(e)}")
        session.rollback()
