import pandas as pd 

# Initial dart data - do not override these CSV files 
bs = pd.read_csv('dart_bs.csv')
cis = pd.read_csv('dart_cis.csv')
cf = pd.read_csv('dart_cf.csv')
incs = pd.read_csv('dart_incs.csv')

corp_with_incs = incs['corp'].unique()

for corp in corp_with_incs: 
    right_index = cis[cis['corp'] == corp].index[-1] 
    
    cis_left = cis.iloc[:right_index + 1]
    cis_right  = cis.iloc[right_index + 1:] 
    
    incs_rows = incs[incs['corp'] == corp]
    
    cis = pd.concat([cis_left, incs_rows, cis_right], ignore_index=True) 
    
# Update csv and MySQL 
cis.to_csv('cis_updated.csv', encoding='utf-8-sig', index=False) 