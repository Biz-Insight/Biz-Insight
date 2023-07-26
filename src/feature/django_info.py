import numpy as np
import pickle
from scipy import stats
import pandas as pd
from sqlalchemy import create_engine


def django_info(revenue, sector):
    # initialization
    user = "multi"
    password = "*****!"
    host = "ec2-15-152-211-160.ap-northeast-3.compute.amazonaws.com"
    database = "Data_Mart"

    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

    query = "SELECT * FROM Data_Mart.sector_revenue_top_features;"
    sector_revenue_top_features = pd.read_sql(query, engine)

    query = "SELECT * FROM Data_Mart.industry_average_year;"
    industry_average = pd.read_sql(query, engine)

    query = "SELECT * FROM Data_Mart.sector_revenue_aggregation;"
    sector_revenue_aggregation = pd.read_sql(query, engine)

    # revenue_group
    ###############################################################################
    input_sectors = [sector]
    new_data = {sector: revenue}

    clustered_sectors = [
        "서비스업",
        "기타금융",
        "운수창고업",
        "음식료품",
        "화학",
        "전기전자",
        "유통업",
        "기계",
        "운수장비",
        "의약품",
        "철강금속",
    ]

    percentile_sectors = [
        "건설업",
        "섬유의복",
        "통신업",
        "전기가스업",
        "종이목재",
        "농업, 임업 및 어업",
        "비금속광물",
        "기타제조업",
    ]

    with open("cluster_label_mappings.pkl", "rb") as f:
        cluster_label_mappings = pickle.load(f)

    with open("sector_revenue_data.pkl", "rb") as f:
        sector_revenue_data = pickle.load(f)

    for sector in input_sectors:
        if sector in clustered_sectors:
            with open(f"{sector}_kmeans_model.pkl", "rb") as file:
                model = pickle.load(file)

            data = new_data[sector]
            data_array = np.array([[data]])
            cluster_label = model.predict(data_array)[0]
            revenue_group = cluster_label_mappings[sector][cluster_label]
        elif sector in percentile_sectors:
            data = new_data[sector]
            data_of_sector = np.array(sector_revenue_data[sector])
            percentile = stats.percentileofscore(data_of_sector, data)
            if percentile < 33:
                revenue_group = "하위"
            elif percentile < 67:
                revenue_group = "중위"
            else:
                revenue_group = "상위"
        else:
            print(f"Unknown sector: {sector}")
    ###############################################################################
    corp_row = sector_revenue_top_features[
        (sector_revenue_top_features["Sector"] == sector)
        & (sector_revenue_top_features["Revenue_Group"] == revenue_group)
    ]

    corr_df = []

    for idx, row in corp_row.iterrows():
        for i in range(1, 6):
            feature = row[f"Top{i}"]
            correlation = row[f"Correlation{i}"]

            corr_df.append(
                {
                    "feature": feature.lower(),
                    "correlation": correlation,
                }
            )
    top_correlation = pd.DataFrame(corr_df)

    ###############################################################################
    # sector_credit_rating
    sector_revenue_aggregation.columns = sector_revenue_aggregation.columns.str.lower()

    sector_filter = sector_revenue_aggregation[
        sector_revenue_aggregation["sector"] == sector
    ]
    sector_credit_rating = sector_filter[
        ["sector", "revenue_group", "rank_value_median"]
    ].reset_index(drop=True)
    ###############################################################################

    return revenue_group, top_correlation, sector_credit_rating
