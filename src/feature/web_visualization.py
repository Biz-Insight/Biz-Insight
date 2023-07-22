import pandas as pd
import warnings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

warnings.filterwarnings("ignore", category=FutureWarning)

username = "multi"
password = "*****!"
hostname = "ec2-15-152-211-160.ap-northeast-3.compute.amazonaws.com"
database_name = "Data_Mart"

desired_table_name = "web_visualization"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{hostname}/{database_name}"
)

Session = sessionmaker(bind=engine)

query = "SELECT * FROM Data_Mart.main_fs;"
main_fs = pd.read_sql(query, engine)

query = "SELECT * FROM Data_Mart.credit_data_web;"
credit_data_web = pd.read_sql(query, engine)

query = "SELECT * FROM Data_Mart.investment_data_web;"
investment_data_web = pd.read_sql(query, engine)

main_fs = main_fs.drop(["fs_type"], axis=1)
credit_data_web = credit_data_web.drop(["id"], axis=1)
investment_data_web = investment_data_web.drop(["id"], axis=1)

web_visualization = pd.concat(
    [main_fs, credit_data_web, investment_data_web], axis=0, ignore_index=True
)

web_visualization.to_csv("web_visualization.csv", encoding="utf-8-sig", index=False)

try:
    with engine.begin() as connection, Session() as session:
        web_visualization.to_sql(
            desired_table_name,
            con=connection,
            if_exists="replace",
            index=False,
            chunksize=1000,
        )
        session.commit()
except Exception as e:
    print(f"An error occurred: {str(e)}")
    session.rollback()
