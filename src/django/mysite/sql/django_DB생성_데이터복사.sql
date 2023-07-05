# DB table 중간에 이름 바꾸면 장고에서 인식 못함... 이름 바꾸지 말고 되도록 한번에 제대로 작업할 것.

# 복사할 데이터 사본 만들기
create table django_test2.preprocessed SELECT * FROM dart_data.preprocessed_tmp;


# 복사할 테이블 컬럼정보 불러오기
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'django_test2' 
  AND table_name = 'preprocessed_tmp';


# 복사한 컬럼정보 django model에 붙여넣기
# 장고 migrations 해서 django로 DB table 생성

# id추가 
ALTER TABLE django_test2.preprocessed_tmp
ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST;


# 테이블 내용 복사
insert into django_test2.credit_mockup
select * from django_test2.preprocessed_tmp;

# 테이블 드랍
drop table django_test2.feature_combined;



