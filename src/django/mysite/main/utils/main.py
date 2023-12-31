from .import_data import *
from .preprocess_data import *
from .prediction_models import *

warnings.filterwarnings("ignore")


def get_credit_rank(input_excel_data):
    # 데이터 불러오기
    data_reviews = import_from_mysql(
        username="root",
        password="****",
        host_ip="127.0.0.1",
        database_name="Data_Mart",
        desired_table_name="employee_reviews_2023",
    )

    data_jaemu = import_from_excel(input_excel_data)

    # DB에 리뷰가 존재하는 기업만 merge
    data_total = merge_data(data_reviews, data_jaemu)

    # 데이터 전처리
    if len(data_total.columns) == 55:
        # padding
        sequences_up_reviews = padding_sequences(
            data_total, up_or_down="up", max_length=50
        )
        sequences_down_reviews = padding_sequences(
            data_total, up_or_down="down", max_length=50
        )

        # jaemu data preprocessing
        scaled_data_jaemu = jaemu_data_preprocessing(data_total)

        pred_rank = dl_model(
            sequences_up_reviews, sequences_down_reviews, scaled_data_jaemu
        )
        print(f"신용등급 예측결과: '{pred_rank}'")

    elif len(data_total.columns) == 52:
        data_jamu = data_total.drop("corp", axis=1)
        pred_rank = rf_model(data_jamu)
        print(f"신용등급 예측결과: '{pred_rank}'")

    else:
        print("error")

    return pred_rank
