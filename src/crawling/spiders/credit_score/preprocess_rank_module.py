sql_query1 = """
SELECT C.corp, C.stock_code, D.sector, C.year, C.kis_bond_type, C.kis_rank, C.nice_bond_type, C.nice_rank
FROM (	SELECT 	B.corp,
			B.stock_code,
			A.year,
			A.kis_bond_type,
			A.kis_rank,
			A.nice_bond_type,
			A.nice_rank	
		FROM (	SELECT 	K.stock_code,
				K.year,
				K.bond_type AS kis_bond_type,
				K.rank AS kis_rank,
				N.bond_type AS nice_bond_type,
				N.rank AS nice_rank
				FROM preprocessed_data.kis_rank_data AS K
				LEFT JOIN preprocessed_data.nice_rank_data AS N 
				ON K.stock_code = N.stock_code 
				AND K.year = N.year
				UNION
				SELECT	N.stock_code,
						N.year,
						K.bond_type AS kis_bond_type,
						K.rank AS kis_rank,
						N.bond_type AS nice_bond_type,
						N.rank AS nice_rank
				FROM preprocessed_data.kis_rank_data AS K
				RIGHT JOIN preprocessed_data.nice_rank_data AS N 
				ON K.stock_code = N.stock_code 
				AND K.year = N.year) AS A
		LEFT JOIN raw_data.corp_list AS B
		ON A.stock_code = B.stock_code) C
LEFT JOIN ( SELECT DISTINCT stock_code, sector FROM dart_data.main_fs) AS D
			ON C.stock_code = D.stock_code;
"""

# rename list
alphabet = [
    ["A", "에이"],
    ["B", "비"],
    ["C", "씨"],
    ["D", "디"],
    ["E", "이"],
    ["F", "에프"],
    ["G", "지"],
    ["H", "에이치"],
    ["I", "아이"],
    ["J", "제이"],
    ["K", "케이"],
    ["L", "엘"],
    ["M", "엠"],
    ["N", "엔"],
    ["O", "오"],
    ["P", "피"],
    ["Q", "큐"],
    ["R", "알"],
    ["S", "에스"],
    ["T", "티"],
    ["U", "유"],
    ["V", "브이"],
    ["W", "더블유"],
    ["X", "엑스"],
    ["Y", "와이"],
    ["Z", "제트"],
    ["&", "앤"],
]


nice_rename_list = [
    ["비엔케이금융지주", "BNK금융지주"],
    ["비엔케이투자증권", "BNK투자증권"],
    ["디비금융투자", "DB금융투자"],
    ["디비손해보험", "DB손해보험"],
    ["디비하이텍", "DB하이텍"],
    ["디지비금융지주", "DGB금융지주"],
    ["디지비캐피탈", "DGB캐피탈"],
    ["에이치에스디엔진", "HSD엔진"],
    ["제이비금융지주", "JB금융지주"],
    ["제이비우리캐피탈", "JB우리캐피탈"],
    ["제이더블유홀딩스", "JW홀딩스"],
    ["케이비캐피탈", "KB캐피탈"],
    ["케이알모터스", "KR모터스"],
    ["엘에프", "LF"],
    ["피오에스씨오", "POSCO"],
    ["엔에이브이이알", "NAVER"],
    ["에스-오아이엘", "S-OIL"],
    ["코오롱인더", "코오롱인더스트리"],
    ["케이비금융", "케이비금융지주"],
    ["에이프로젠바이오로직스", "에이프로젠제약"],
]


kis_rename_list = [
    ["에이제이네트웍스", "AJ네트웍스"],
    ["비엔케이금융지주", "BNK금융지주"],
    ["씨제이제일제당", "CJ제일제당"],
    ["디비손해보험", "DB손해보험"],
    ["디비캐피탈", "DB캐피탈"],
    ["디지비금융지주", "DGB금융지주"],
    ["이1", "E1"],
    ["지에스", "GS"],
    ["에이치에스디엔진", "HSD엔진"],
    ["제이비금융지주", "JB금융지주"],
    ["케이비금융", "KB금융지주"],
    ["엘에프", "LF"],
    ["엘지유플러스", "LG유플러스"],
    ["엘지전자", "LG전자"],
    ["엘지화학", "LG화학"],
    ["엘에스", "LS"],
    ["엘엑스인터네셔널", "LX인터내셔널"],
    ["OCI홀딩스", "OCI"],
    ["에스-오IL", "S-OIL"],
    ["에스비에스", "SBS"],
    ["에스케이씨", "SKC"],
    ["에스케이가스", "SK가스"],
    ["에스케이네트웍스", "SK네트웍스"],
    ["에스케이이노베이션", "SK이노베이션"],
    ["에스케이증권", "SK증권"],
    ["에스케이텔레콤", "SK텔레콤"],
    ["피오에스씨오", "POSCO"],
    ["엔에이브이이알", "NAVER"],
]


# preprocess module
def kis_preprocess(data):
    # 불필요한 컬럼 제거
    drop = data.drop("evaluate_type", axis=1)

    # 정렬
    sorted = drop.sort_values(["corp_name", "month"], ascending=True)

    # 최신만 남겨놓고 제거
    duplicate = sorted.drop_duplicates(subset="corp_name", keep="last")

    # 재배치
    new_columns = ["corp_name", "year", "month", "day", "bond_type", "rank"]
    reorder = duplicate.reindex(columns=new_columns)

    return reorder


def nice_preprocess(data):
    # 날짜 생성
    data[["year", "month", "day"]] = data["등급확정일"].str.split(".", expand=True)

    # 불필요한 컬럼 제거
    drop1 = data.drop(data.index[data["현재"] == "취소"])
    drop2 = drop1.drop(
        [
            "회차",
            "상환순위",
            "평정",
            "직전",
            "등급결정일\n(평가일)",
            "등급확정일",
            "Unnamed: 6",
            "Unnamed: 8",
            "발행액(억원)",
        ],
        axis=1,
    )

    # 정렬
    sort = drop2.sort_values(["기업명", "month"])

    # 최신만 남겨놓고 제거
    duplicated = sort.drop_duplicates(subset="기업명", keep="last")

    # 재배치
    new_columns = ["기업명", "year", "month", "day", "종류", "현재"]
    reorder = duplicated.reindex(columns=new_columns)

    # (재), (주) 제거 및 컬럼명 재지정
    rename = reorder.rename(columns={"기업명": "corp", "종류": "bond_type", "현재": "rank"})
    rename["corp"] = rename["corp"].str.replace(r"\(재\)|\(주\)", "", regex=True)

    return rename


# SQL
def import_from_mysql(username, password, host_ip, database_name, desired_table_name):
    import pymysql
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    hostname = f"ec2-{host_ip}.ap-northeast-3.compute.amazonaws.com"

    connection_str = f"mysql+pymysql://{username}:{password}@{hostname}/{database_name}"
    engine = create_engine(connection_str)
    query = f"SELECT * FROM {desired_table_name}"

    df = pd.read_sql(query, engine)

    return df


def export_to_mysql(df, username, password, host_ip, database_name, desired_table_name):
    import pymysql
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    hostname = f"ec2-{host_ip}.ap-northeast-3.compute.amazonaws.com"

    cnx = pymysql.connect(user=username, password=password, host=hostname)
    cursor = cnx.cursor()

    engine = create_engine(
        "mysql+pymysql://{user}:{pw}@{host}/{db}".format(
            user=username, pw=password, db=database_name, host=hostname
        )
    )

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Change df name
        df.to_sql(
            desired_table_name,
            con=engine,
            if_exists="replace",
            index=False,
            chunksize=1000,
        )
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    cursor.close()
    cnx.close()
