from .settings1 import *
import os
import pickle
from django.conf import settings


rank_mapping = {
    "AAA": 9,
    "AA+": 8,
    "AA": 7,
    "AA-": 6,
    "A+": 5,
    "A": 4,
    "A-": 3,
    "BBB": 2,
    "JB": 1,
}


def rf_model(data_jamu):
    current_dir = os.path.join(settings.BASE_DIR, "static")
    file_path = os.path.join(current_dir, "rf_model.pkl")
    with open(file_path, "rb") as f:
        clf = pickle.load(f)

    rank = clf.predict(data_jamu)
    rank_prediction = clf.predict(data_jamu)

    rank_mapping_reverse = {v: k for k, v in rank_mapping.items()}
    prediction = rank_mapping_reverse[rank_prediction[0]]

    return prediction


def dl_model(sequences_up_reviews, sequences_down_reviews, scaled_data_jaemu):
    loss_func = SparseCategoricalFocalLoss(gamma=2)

    with tf.keras.utils.custom_object_scope(
        {"sparse_categorical_focal_loss": loss_func}
    ):
        # Specify the file path (without Korean characters)
        h5_model_path = "./dl_model.h5"

        # Load the model using the file path
        loaded_model = tf.keras.models.load_model(h5_model_path)

    predict_test = loaded_model.predict(
        [sequences_up_reviews, sequences_down_reviews, scaled_data_jaemu]
    )

    predicted_classes = np.argmax(predict_test, axis=1)

    rank = statistics.mode(predicted_classes)

    return (
        str(rank)
        .replace("0", "JB")
        .replace("1", "BBB")
        .replace("2", "A-")
        .replace("3", "A")
        .replace("4", "A+")
        .replace("5", "AA-")
        .replace("6", "AA")
        .replace("7", "AA+")
        .replace("8", "AAA")
    )
