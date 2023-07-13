import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymysql

from data_processor import process_company_data
from data_saver import save_to_csv


def process_and_save_companies(company_list, file_names, start=0, end=None):
    data_frames = {
        "bs": pd.DataFrame(),
        "cis": pd.DataFrame(),
        "cf": pd.DataFrame(),
        "incs": pd.DataFrame(),
    }

    error_count = 0
    for index, company in enumerate(company_list[start:end]):
        bs_ra = cis_ra = cf_ra = incs_ra = None
        try:
            bs_ra, cis_ra, cf_ra, incs_ra = process_company_data(company)
            print(f"Successfully obtained data for Company {index}")

        except Exception as e:
            print(f"Error occurred for {company}: {str(e)}")
            error_count += 1
            continue

        data_frames["bs"] = pd.concat(
            [data_frames["bs"], bs_ra], axis=0, ignore_index=True
        )
        data_frames["cis"] = pd.concat(
            [data_frames["cis"], cis_ra], axis=0, ignore_index=True
        )
        data_frames["cf"] = pd.concat(
            [data_frames["cf"], cf_ra], axis=0, ignore_index=True
        )
        if incs_ra is not None:
            data_frames["incs"] = pd.concat(
                [data_frames["incs"], incs_ra], axis=0, ignore_index=True
            )

    print(f"Failed to obtain data for {error_count} Companies")

    for index, key in enumerate(data_frames.keys()):
        save_to_csv(data_frames[key], file_names[index])

    bs = pd.read_csv("bs.csv")
    cis = pd.read_csv("cis.csv")
    cf = pd.read_csv("cf.csv")
    incs = pd.read_csv("incs.csv")

    corp_with_incs = incs["corp"].unique()

    for corp in corp_with_incs:
        right_index = cis[cis["corp"] == corp].index[-1]

        cis_left = cis.iloc[: right_index + 1]
        cis_right = cis.iloc[right_index + 1 :]

        incs_rows = incs[incs["corp"] == corp]

        cis = pd.concat([cis_left, incs_rows, cis_right], ignore_index=True)

    incs = cis.copy()

    incs = incs.drop_duplicates()

    bs_with_statement = bs.copy()
    bs_with_statement["fs_type"] = "bs"

    incs_with_statement = incs.copy()
    incs_with_statement["fs_type"] = "incs"

    cf_with_statement = cf.copy()
    cf_with_statement["fs_type"] = "cf"

    fs = pd.concat(
        [bs_with_statement, incs_with_statement, cf_with_statement], ignore_index=True
    )

    cols = ["fs_type"] + [col for col in fs.columns if col != "fs_type"]
    fs = fs[cols]

    bs.to_csv("bs.csv", encoding="utf-8-sig", index=False)
    incs.to_csv("incs.csv", encoding="utf-8-sig", index=False)
    cf.to_csv("cf.csv", encoding="utf-8-sig", index=False)
    fs.to_csv("fs.csv", encoding="utf-8-sig", index=False)

    username = "multi"
    password = "Campus123!"
    hostname = "ec2-15-152-211-160.ap-northeast-3.compute.amazonaws.com"
    database_name = "Data_Lake"

    engine = create_engine(
        "mysql+pymysql://{user}:{pw}@{host}/{db}".format(
            user=username, pw=password, db=database_name, host=hostname
        )
    )

    Session = sessionmaker(bind=engine)
    session = Session()

    dataframes = {"bs": bs, "incs": incs, "cf": cf, "fs": fs}

    try:
        for table_name, df in dataframes.items():
            df.to_sql(
                table_name, con=engine, if_exists="replace", index=False, chunksize=1000
            )
            session.commit()
    except Exception as e:
        session.rollback()
        print("An error occurred:", e)
    finally:
        session.close()
