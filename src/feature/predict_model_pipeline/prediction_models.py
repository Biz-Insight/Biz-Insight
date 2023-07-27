from settings import *


def rf_model(scaled_data_jaemu):
    with open("rf_model.pkl", "rb") as file:
        clf = pickle.load(file)

    rank = clf.predict(scaled_data_jaemu)

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
