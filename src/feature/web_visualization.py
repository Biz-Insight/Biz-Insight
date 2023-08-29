import pandas as pd
import warnings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_utils import (
    save_data_to_csv,
    save_data_to_database,
)

warnings.filterwarnings("ignore", category=FutureWarning)

username = "root"
password = "****"
hostname = "localhost"
database_name = "Data_Mart"
DB_URL = f"mysql+pymysql://{username}:{password}@{hostname}/{database_name}"

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
# credit_data_web = credit_data_web.drop(["id"], axis=1)
# investment_data_web = investment_data_web.drop(["id"], axis=1)

web_visualization = pd.concat(
    [main_fs, credit_data_web, investment_data_web], axis=0, ignore_index=True
)

save_data_to_csv(web_visualization, "web_visualization.csv")

save_data_to_database(web_visualization, "web_visualization", DB_URL)
