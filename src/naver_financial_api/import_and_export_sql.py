def import_from_mysql(username, password, host_ip, database_name, desired_table_name):

    import pymysql
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    hostname = f'ec2-{host_ip}.ap-northeast-3.compute.amazonaws.com'

    connection_str = f'mysql+pymysql://{username}:{password}@{hostname}/{database_name}'
    engine = create_engine(connection_str)
    query = f'SELECT * FROM {desired_table_name}'

    df = pd.read_sql(query, engine)

    return df

def export_from_mysql(df, username, password, host_ip, database_name, desired_table_name):

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
        df.to_sql(desired_table_name, con=engine, if_exists='replace', index=False, chunksize = 1000) 
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    cursor.close() 
    cnx.close()