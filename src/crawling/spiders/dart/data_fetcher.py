import dart_fss as dart

API_KEY = "ABC123"


def get_corp_list():
    dart.set_api_key(api_key=API_KEY)
    corp_list = dart.get_corp_list()
    kospi_list = corp_list.find_by_corp_name(corp_name="", market="Y")
    return kospi_list
