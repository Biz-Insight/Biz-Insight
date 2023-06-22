# 삼성 재무제표 테이블 생성
from decimal import Decimal
from settings import *

mydb = get_mysql_connection("host", "user", "password", "database")
mycursor = mydb.cursor()

# ss_name 테이블 칼럼
ss_name_c = [
    "corp",
    "account",
    "account_detail",
    "2018",
    "2019",
    "2020",
    "2021",
    "2022",
]

ss_table = f"CREATE TABLE IF NOT EXISTS `samsung_bs` ("
for column in ss_name_c:
    if column == "corp" or column == "account" or column == "account_detail":
        ss_table += f"`{column}` VARCHAR(255), "
    else:
        ss_table += f"`{column}` DECIMAL(60), "
ss_table = ss_table[:-2] + ")"

mycursor.execute(ss_table)

file_path = os.path.join("data", "ss_bs.csv")

# 파일 읽기 & DB에 데이터 삽입
with open(file_path, encoding="cp949") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        # 데이터 삽입
        insert_row_sql = f"INSERT INTO `samsung_bs` (`{ss_name_c[0]}`, `{ss_name_c[1]}`, `{ss_name_c[2]}`, `{ss_name_c[3]}`, `{ss_name_c[4]}`, `{ss_name_c[5]}`, `{ss_name_c[6]}`, `{ss_name_c[7]}`) VALUES ('{row[0]}', '{row[6]}', '{row[2]}', {row[13]}, {Decimal(row[12])}, {Decimal(row[11])}, {Decimal(row[10])}, {Decimal(row[9])})"
        mycursor.execute(insert_row_sql)

mydb.commit()
mydb.close()
