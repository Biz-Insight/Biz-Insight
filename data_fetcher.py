import dart_fss as dart
from config import api_key

def get_corp_list():
    dart.set_api_key(api_key=api_key)
    corp_list = dart.get_corp_list()
    kospi_list = corp_list.find_by_corp_name(corp_name='', market='Y')
    return kospi_list
