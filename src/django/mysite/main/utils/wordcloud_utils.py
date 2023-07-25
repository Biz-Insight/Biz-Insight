import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from wordcloud import WordCloud
import os
from django.conf import settings
import matplotlib

matplotlib.use("Agg")

csv_file_path = os.path.join(settings.BASE_DIR, "main", "utils", "wordcloud.csv")
pre_df = pd.read_csv(csv_file_path, encoding="utf-8")
sns.color_palette("Set2")


def i_strip(i):
    if type(i) == str:
        i = i.split(", ")
        word = i[0].strip("'")
        pos = i[-1].strip("'")
    else:
        word = i[0]
        pos = i[-1]
    return word, pos


def wordCloud(text_df, stop_words, val, token):
    # for val in iter_value_list:
    print(val, "WordCloud")
    FEATURE_POS = [
        # 부사
        "MAG",
        "MAJ",
        "MM",
        # 명사
        "NNB",
        "NNBC",
        "NNG",
        "NNP",
        "NP",
        # 형용사, 동사
        "VA",
        "VV",
    ]
    documents = []
    for row in pre_df[pre_df["corp"] == val][token]:
        morphs = ""
        if type(row) == str:
            row = row.strip("[").strip("]").strip("(").strip(")").split("), (")
        for i in row:
            word, pos = i_strip(i)
            if pos not in FEATURE_POS:
                continue
            if word not in stop_words:
                morphs = morphs + word + " "
        documents.append(morphs)
    vectorizer = TfidfVectorizer()
    vecs = vectorizer.fit_transform(documents)
    dense = vecs.todense()
    lst1 = dense.tolist()
    df_tfidf = pd.DataFrame(lst1, columns=vectorizer.get_feature_names_out())
    Cloud = WordCloud(
        font_path=os.path.join(
            settings.BASE_DIR, "static/fonts/NanumSquareNeo-cBd.ttf"
        ),
        width=700,  # 워드클라우드의 너비
        height=350,  # 워드클라우드의 높이
        relative_scaling=0.2,
        background_color="white",
        max_words=300,
        colormap="Set2",
    ).generate_from_frequencies(df_tfidf.T.sum(axis=1))

    fig, ax = plt.subplots()  # 변경된 부분
    ax.imshow(Cloud, interpolation="bilinear")
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])  # 여백 제거

    save_path = os.path.join(
        settings.BASE_DIR, "static", f"wordcloud_images/{val}_{token}_wordcloud.png"
    )
    plt.savefig(save_path, bbox_inches="tight", pad_inches=0)  # 여백 제거
    # plt.show()  # 이 부분은 필요없으면 주석 처리합니다.
    plt.close()
    return


# # 사용 예시
# stop_words = ["단점, 장점"]
# wordCloud(pre_df, stop_words, "롯데지주", "up_morphs")  # 장점
# wordCloud(pre_df, stop_words, "롯데지주", "down_morphs")  # 장점
