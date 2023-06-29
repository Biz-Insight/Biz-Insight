def import_from_mysql(username, password, host_ip, database_name, desired_table_name):

    import pymysql
    import pandas as pd
    from sqlalchemy import create_engine

    hostname = f'ec2-{host_ip}.ap-northeast-3.compute.amazonaws.com'

    connection_str = f'mysql+pymysql://{username}:{password}@{hostname}/{database_name}'
    engine = create_engine(connection_str)
    query = f'SELECT * FROM {desired_table_name}'

    return pd.read_sql(query, engine)

def export_to_mysql(df, username, password, host_ip, database_name, desired_table_name):

    import pymysql
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    hostname = f'ec2-{host_ip}.ap-northeast-3.compute.amazonaws.com'

    #cnx = pymysql.connect(user=username, password=password, host=hostname)
    #cursor = cnx.cursor() 

    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}" \
                        .format(user=username,
                                pw=password,
                                db=database_name,
                                host=hostname))
                                
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Change df name 
        df.to_sql(desired_table_name, con=engine, if_exists='replace', index=False, chunksize = 1000) 
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    #cursor.close() 
    #cnx.close()

def insert_to_mysql(df, username, password, host_ip, database_name, desired_table_name):

    import pymysql
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    hostname = f'ec2-{host_ip}.ap-northeast-3.compute.amazonaws.com'

    cnx = pymysql.connect(user=username, password=password, host=hostname)
    cursor = cnx.cursor() 

    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}" \
                        .format(user=username,
                                pw=password,
                                db=database_name,
                                host=hostname))
                                
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Change df name 
        df.to_sql(desired_table_name, con=engine, if_exists='append', index=False, chunksize = 1000) 
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    #cursor.close() 
    #cnx.close()


def crawl_realtime_data(df, today):

    import urllib.request
    import pandas as pd
    import json

    corp_list = df.values.tolist()

    realtime_list = []

    for corp_set in corp_list:
        item_name = corp_set[0]
        item_code = corp_set[1]
        url = f"https://api.finance.naver.com/service/itemSummary.nhn?itemcode={item_code}"

        raw_data = urllib.request.urlopen(url).read()
        json_data = json.loads(raw_data)
        
        ######################################
        crawl_dict = {}

        crawl_dict['corp'] = item_name
        crawl_dict['stock_code'] = item_code
        crawl_dict['date'] = today
        crawl_dict['marketSum'] = json_data['marketSum']
        crawl_dict['per'] = json_data['per']
        crawl_dict['eps'] = json_data['eps']
        crawl_dict['pbr'] = json_data['pbr']
        crawl_dict['now'] = json_data['now']
        ######################################

        print(f'{today} : {item_name}, done.')

        realtime_list.append(crawl_dict)

    return pd.DataFrame(realtime_list)

def crawl_stock_price(df, start_time, end_time, time_frame):
    from urllib import parse
    from ast import literal_eval
    import requests
    import pandas as pd

    corp_list = df.values.tolist()

    corp_stock_price_df = pd.DataFrame(columns=['날짜', '시가', '고가', '저가', '종가', '거래량', '외국인소진율', 'stock_code', 'corp'])

    for corp_num in corp_list:
        item_name = corp_num[0]
        item_code = corp_num[1]

        get_param = {
            'symbol': item_code,
            'requestType': 1,
            'startTime': start_time,
            'endTime': end_time,
            'timeframe': time_frame
        }

        get_param = parse.urlencode(get_param)
        url = "https://api.finance.naver.com/siseJson.naver?%s" % get_param
        response = requests.get(url)

        stock_df = pd.DataFrame(data=literal_eval(response.text.strip())[1:], columns=literal_eval(response.text.strip())[0])

        stock_df['stock_code'] = item_code
        stock_df['corp'] = item_name

        corp_stock_price_df = pd.concat([corp_stock_price_df, stock_df], axis=0)

        print(item_name + 'is done.')

    corp_stock_price_df = corp_stock_price_df[['corp', 'stock_code', '날짜', '시가', '고가', '저가', '종가', '거래량', '외국인소진율']]

    output_df = corp_stock_price_df.rename(columns={'날짜': 'date',
                                                    '시가': 'open',
                                                    '고가': 'high',
                                                    '저가': 'low',
                                                    '종가': 'close',
                                                    '거래량': 'amount',
                                                    '외국인소진율': 'foreign_ownership_ratio'})

    output_df['date'] = pd.to_datetime(output_df['date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')

    return output_df