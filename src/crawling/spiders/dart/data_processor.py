import pandas as pd

def insert_company_info(df, company, indices=(0, 1, 2)):
    columns = ['corp', 'stock_code', 'sector']
    values = [company.corp_name, company.stock_code, company.sector]
    
    for index, column, value in zip(indices, columns, values):
        df.insert(index, column, value)
    return df 

def refactor_df(df):
    def rename_columns(col):
        if col[0].isdigit() or col[0][:8].isnumeric():
            return col[0][:4]
        elif col[0] == 'corp' or col[0] == 'stock_code' or col[0] == 'sector': 
            return col[0] 
        else:
            return col[1]

    def ensure_columns_exist_at_index(df):
        cols_to_ensure = [('class3', 9), ('class4', 10)]
        for col, desired_idx in cols_to_ensure:
            if len(df.columns) <= desired_idx or df.columns[desired_idx] != col:
                df.insert(loc=desired_idx, column=col, value=None)
        return df

    def ensure_year_columns_exist(df):
        year_cols_to_ensure = [('2022', 11), ('2021', 12), ('2020', 13),
                               ('2019', 14), ('2018', 15)]
        for col, desired_idx in year_cols_to_ensure:
            if len(df.columns) <= desired_idx or \
                df.columns[desired_idx] != col:
                df.insert(loc=desired_idx, column=col, value=None)
        return df
    
    new_columns = [rename_columns(col) for col in df.columns]
    df = df.set_axis(new_columns, axis=1)
    df = ensure_columns_exist_at_index(df)
    df = ensure_year_columns_exist(df)
    
    return df
    
def rearrange_df(df): 
    new_order = ['corp', 'stock_code', 'sector', 'label_en', 'label_ko',
                 'class1', 'class2', 'class3', 'class4', '2018', '2019',
                 '2020', '2021', '2022']
    df = df[new_order] 
    return df 


def process_company_data(company):
    fs = company.extract_fs(bgn_de='20210101')
    bs, cis, cf, incs = fs['bs'], fs['cis'], fs['cf'], fs['is']

    insert_company_info(bs, company=company)
    insert_company_info(cis, company=company)
    insert_company_info(cf, company=company)
    
    bs_rf = refactor_df(bs)
    cis_rf = refactor_df(cis)
    cf_rf = refactor_df(cf)

    bs_ra = rearrange_df(bs_rf)
    cis_ra = rearrange_df(cis_rf)
    cf_ra = rearrange_df(cf_rf)
    
    if incs is not None:
        insert_company_info(incs, company=company)
        incs_rf = refactor_df(incs)
        incs_ra = rearrange_df(incs_rf)
    else:
        incs_ra = None

    return bs_ra, cis_ra, cf_ra, incs_ra
