# kospi 상장된 기업 테이블 생성
from settings import *


mydb = get_mysql_connection("host", "user", "password", "database")
mycursor = mydb.cursor()

# company_name 테이블 칼럼
company_name_c = ["Standard_code", "Short_code", "Company_full_name", "Company_name"]

company_table = f"CREATE TABLE IF NOT EXISTS `company_name` ("
for column in company_name_c:
    company_table += (
        f"`{column}` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci, "
    )
company_table = company_table[:-2] + ")"

mycursor.execute(company_table)

file_path = os.path.join("data", "kospi_c_name.csv")

# 파일 읽기 & DB에 데이터 삽입
with open(file_path, encoding="cp949") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        # 데이터 삽입
        insert_row_sql = f"INSERT INTO `company_name` (`{company_name_c[0]}`, `{company_name_c[1]}`, `{company_name_c[2]}`, `{company_name_c[3]}`) VALUES ('{row[2]}', '{row[3]}', '{row[0]}', '{row[1]}')"
        mycursor.execute(insert_row_sql)


mydb.commit()
mydb.close()
