import pandas as pd 
from data_saver import save_to_csv
from data_processor import process_company_data

def process_and_save_companies(kospi_list, file_names, start=0, end=None):
    data_frames = {
        'bs': pd.DataFrame(),
        'cis': pd.DataFrame(),
        'cf': pd.DataFrame(),
        'incs': pd.DataFrame()
    }
    
    error_count = 0
    for company in kospi_list[start:end]:
        bs_ra = cis_ra = cf_ra = incs_ra = None
        try:
            bs_ra, cis_ra, cf_ra, incs_ra = process_company_data(company)
        except Exception as e:
            print(f"Error occurred for {company}: {str(e)}")
            error_count += 1
            continue

        data_frames['bs'] = pd.concat([data_frames['bs'], bs_ra], axis=0,
                                      ignore_index=True)
        data_frames['cis'] = pd.concat([data_frames['cis'], cis_ra], axis=0,
                                       ignore_index=True)
        data_frames['cf'] = pd.concat([data_frames['cf'], cf_ra], axis=0,
                                      ignore_index=True)
        if incs_ra is not None:
            data_frames['incs'] = pd.concat([data_frames['incs'], incs_ra],
                                            axis=0, ignore_index=True)

    print(f"Error Count: {error_count}")
    
    for index, key in enumerate(data_frames.keys()):
        save_to_csv(data_frames[key], file_names[index])

