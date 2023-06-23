from data_fetcher import get_corp_list
from process_save import process_and_save_companies

def main():
    
    kospi_list = get_corp_list()
    
    file_names = ['dart_bs.csv', 'dart_cis.csv', 'dart_cf.csv', 'dart_is.csv']
    process_and_save_companies(kospi_list, file_names, start=0, end=None)
    
if __name__ == "__main__":
    main()
