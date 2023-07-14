from data_fetcher import get_corp_list
from process_save import process_and_save_companies


def main():
    kospi_list = get_corp_list()

    file_names = ["bs.csv", "cis.csv", "cf.csv", "incs.csv"]
    # Crawls KOSPI data, processes the financial statements into
    # bs, incs, cf, fs and saves them in CSV and into MySQL Database
    process_and_save_companies(kospi_list, file_names, start=0, end=None)


if __name__ == "__main__":
    main()
