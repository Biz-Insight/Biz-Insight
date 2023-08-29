import pymysql
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def save_data_to_csv(data, filename):
    data.to_csv(filename, encoding="utf-8-sig", index=False)


def save_data_to_database(data, table_name, DB_URL):
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    try:
        with engine.begin() as connection, Session() as session:
            data.to_sql(
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
