# 🏢 BIZ-INSIGHT 🏢

비즈인사이트는 금융/데이터 전문가는 아니지만, 

비즈니스 의사 결정을 수행해야하는 기업 관계자를 타겟으로 하는  기업별 투자, 신용 정보 맞춤 분석 서비스 입니다.

- 흩어져 있는 투자, 신용 정보를 종합적으로 제공하여 효율적 의사결정에 도움
- 데이터 입력 시 사용자 맞춤 실시간 분석 서비스 제공

![메인페이지](https://github.com/Biz-Insight/Biz-Insight/assets/121608383/580a4d22-829f-4402-aae3-d77fbf3768b1)

## 📢 주요 기능

☑️ 검색가능 기업 목록 조회

![기업리스트](https://github.com/Biz-Insight/Biz-Insight/assets/121608383/a463645b-dc07-42be-880d-b8b940fb0b23)

☑️ 기업개요
- 해당 기업에 대한 기본적인 정보 및 평점, 주가 그래프
- 신용등급 유무에 따른 실제 값 또는 예측 값
- 사내 직원 리뷰에 따른 기업 장단점 워드 클라우드
- GPT가 생각하는 기업에 대한 평가
   
![기업개요](https://github.com/Biz-Insight/Biz-Insight/assets/121608383/efec9ce5-9a59-4101-be18-56ce30aad2d7)

☑️ 재무분석
- 동일 산업군과의 비교 분석
- 주요지표들에 대한 시각화 기능
   
![재무분석800](https://github.com/Biz-Insight/Biz-Insight/assets/121608383/61c91db1-60a5-41d5-8ecf-3256ff4ae9c6)

☑️ 신용분석
- 신용예측에 중요했던 요인들
- 산업, 기업규모별 신용등급과 상관관계가 높았던 피쳐들 확인

✔️ 삼성전자

![신용분석 - 삼전](https://github.com/Biz-Insight/Biz-Insight/assets/121608383/fc64a583-df2e-4d94-8f6e-85ca7831b6e8)

✔️   풀무원

![신용분석 - 풀무원](https://github.com/Biz-Insight/Biz-Insight/assets/121608383/d3fb512f-8ce1-4d6c-a497-3d34ab72af93)

☑️ 상세지표
- 투자, 신용 등 기업분석을 위한 상세지표 확인
   
![상세지표](https://github.com/Biz-Insight/Biz-Insight/assets/121608383/ba4a7743-d5ce-4497-847b-4ff023c41bd9)

☑️ 재무제표 업로드
- 신용등급이 없는 사용자기업에 대한 신용분석 인사이트 제공

![사용자기업](https://github.com/Biz-Insight/Biz-Insight/assets/121608383/85f87702-13d1-49db-b82b-0d0fb1d9f3dc)




---
## 📝 Description

### Data Source
- 재무데이터
	- DART
  
- 신용등급데이터
	- NICE
	- 한국신용평가
	- 한국기업평가

- 직원평가데이터
	- 블라인드
	- 잡플래닛

- 경제지표
	- 한국은행 경제통계시스

### Data Base
![image](https://github.com/Biz-Insight/Biz-Insight/assets/121608383/6eed095f-a2b3-49da-85e0-dd90bf634d12)

### Files
```
data: 수집된 데이터셋 csv 파일

src 
  ├─ db: 데이터 별 db 적재 및 전처리 파이프라인
  │    
  ├─ crawling: 데이터별 수집 크롤러
  │    
  ├─ django/miste: 웹 서비스
  │    
  ├─ eda: 데이터 별 eda
  │   
  └─ feature : 서비스 기능 (신용등급 분석, 데이터 트랜스포메이션, 시각화 등)
```

### Environment
```
Python (v3.9.7|Window)
Django (v2.1.7)
Node.js (v19.4.0)
jQuery (v3.5.1)
Chart.js (v2.8.0)
```


### Prerequisite 
```
seaborn
pandas
scikit-learn

pymysql
mysqlclient
sqlalchemy

requests
tensorflow
wordcloud
tqdm
tokenizers
sentencepiece
focal_loss
```

### Usage
```
$ python src/django/mysite/manage.py runserver
```
