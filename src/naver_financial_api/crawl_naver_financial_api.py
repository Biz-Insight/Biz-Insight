from import_and_export_sql import *

#import data from sql
import_df = import_from_mysql(username = 'multi',
                              password = 'Campus123!',
                              host_ip = '15-152-211-160',
                              database_name = 'raw_data',
                              desired_table_name ='corp_list')

#crawl
import urllib.request
import pandas as pd
import json

corp_list = import_df.values.tolist()

corp_info_list = []

for corp_set in corp_list:
    item_name = corp_set[0]
    item_code = corp_set[1]
    url = f"https://api.finance.naver.com/service/itemSummary.nhn?itemcode={item_code}"

    raw_data = urllib.request.urlopen(url).read()
    json_data = json.loads(raw_data)
    
    ######################################
    market_sum = json_data['marketSum']
    per = json_data['per']
    eps = json_data['eps']
    pbr = json_data['pbr']
    now = json_data['now']
    ######################################

    print(f'corp : {item_name}, done.')
    
    corp_dict = {}

    corp_dict['corp'] = item_name
    corp_dict['stock_code'] = item_code
    corp_dict['marketSum'] = market_sum
    corp_dict['per'] = per
    corp_dict['eps'] = eps
    corp_dict['pbr'] = pbr
    corp_dict['now'] = now

    corp_info_list.append(corp_dict)
    
corp_info_df = pd.DataFrame(corp_info_list)

#export data to sql
export_from_mysql(df = corp_info_df,
                  username = 'multi',
                  password = 'Campus123!',
                  host_ip = '15-152-211-160',
                  database_name = 'raw_data',
                  desired_table_name ='corp_list')




