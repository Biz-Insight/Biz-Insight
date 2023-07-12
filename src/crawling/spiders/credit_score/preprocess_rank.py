# import
from preprocess_corp_credit_rank_module import *
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

kis_2019 = pd.read_csv("./kis_2019.csv", encoding="cp949")
kis_2020 = pd.read_csv("./kis_2020.csv", encoding="cp949")
kis_2021 = pd.read_csv("./kis_2021.csv", encoding="cp949")
kis_2022 = pd.read_csv("./kis_2022.csv", encoding="cp949")
kis_2023 = pd.read_csv("./kis_2023.csv", encoding="cp949")

nice_2019 = pd.read_excel("./nice_2019_raw.xls", skiprows=1).drop(0)
nice_2020 = pd.read_excel("./nice_2020_raw.xls", skiprows=1).drop(0)
nice_2021 = pd.read_excel("./nice_2021_raw.xls", skiprows=1).drop(0)
nice_2022 = pd.read_excel("./nice_2022_raw.xls", skiprows=1).drop(0)
nice_2023 = pd.read_excel("./nice_2023_raw.xls", skiprows=1).drop(0)

# preprocess
processed_nice_2019 = nice_preprocess(data=nice_2019)
processed_nice_2020 = nice_preprocess(data=nice_2020)
processed_nice_2021 = nice_preprocess(data=nice_2021)
processed_nice_2022 = nice_preprocess(data=nice_2022)
processed_nice_2023 = nice_preprocess(data=nice_2023)

# processed_kis_2019 = kis_preprocess(data = kis_2019)
# processed_kis_2020 = kis_preprocess(data = kis_2020)
# processed_kis_2021 = kis_preprocess(data = kis_2021)
# processed_kis_2022 = kis_preprocess(data = kis_2022)
# processed_kis_2023 = kis_preprocess(data = kis_2023)

# concat & duplicate
concat_nice = pd.concat(
    [
        processed_nice_2019,
        processed_nice_2020,
        processed_nice_2021,
        processed_nice_2022,
        processed_nice_2023,
    ],
    ignore_index=True,
)
concat_kis = pd.concat(
    [kis_2019, kis_2020, kis_2021, kis_2022, kis_2023], ignore_index=True
)

concat_kis = concat_kis.drop_duplicates(["corp", "year"], keep="first")
concat_nice = concat_nice.drop_duplicates(["corp", "year"], keep="first")

# import corp_code
import_df = import_from_mysql(
    username="multi",
    password="Campus123!",
    host_ip="15-152-211-160",
    database_name="raw_data",
    desired_table_name="corp_list",
)

stock_code = import_df[["corp", "stock_code"]].drop_duplicates("corp")

# kis renaming
kis_stock_code = import_df[["corp", "stock_code"]].drop_duplicates("corp")

kis_df = (
    concat_kis[["corp", "year", "bond_type", "rank"]]
    .sort_values(["corp", "year"])
    .reset_index(drop=True)
)

for row in range(len(kis_stock_code)):
    for i, j in alphabet:
        kis_stock_code.iloc[row]["corp"] = (
            kis_stock_code.iloc[row]["corp"].upper().replace(i, j)
        )


merge_kis_df = kis_df.merge(kis_stock_code, on="corp", how="left")

# + SK 직접입력
merge_kis_df.loc[merge_kis_df.index[merge_kis_df["corp"] == "SK"]] = merge_kis_df.loc[
    merge_kis_df.index[merge_kis_df["corp"] == "SK"]
].fillna("034730")
merge_kis_df.loc[merge_kis_df.index[merge_kis_df["corp"] == "SK"]]

total_kis_df = merge_kis_df.drop(merge_kis_df.index[merge_kis_df["stock_code"].isna()])
total_kis_df.to_csv("./total_kis_df.csv", encoding="cp949")


# nice renaming
nice_stock_code = import_df[["corp", "stock_code"]].drop_duplicates("corp")

nice_df = (
    concat_nice[["corp", "year", "bond_type", "rank"]]
    .sort_values(["corp", "year"])
    .reset_index(drop=True)
)

for row in range(len(nice_stock_code)):
    for i, j in alphabet:
        nice_stock_code.iloc[row]["corp"] = (
            nice_stock_code.iloc[row]["corp"].upper().replace(i, j)
        )

merge_nice_df = nice_df.merge(nice_stock_code, on="corp", how="left")

total_nice_df = merge_nice_df.drop(
    merge_nice_df.index[merge_nice_df["stock_code"].isna()]
)
total_nice_df.to_csv("./total_nice_df.csv", encoding="cp949")

# export
rank_final = import_from_mysql(
    username="multi",
    password="Campus123!",
    host_ip="15-152-211-160",
    database_name="Data_Warehouse",
    desired_table_name="corp_rank_temp",
)

rank_final.to_csv("./rank_final.csv", index=False, encoding="cp949")

rank_rfinal = pd.read_csv("rank_final_1.csv", encoding="cp949")
rank_rfinal["year"] = (rank_rfinal["year"] - 1).astype("str")

export_to_mysql(
    df=rank_rfinal,
    username="multi",
    password="Campus123!",
    host_ip="15-152-211-160",
    database_name="Data_Warehouse",
    desired_table_name="credit_rank",
)
