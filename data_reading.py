#fastparquet model is needed. If not available, please type in 'pip install fastparquet' prior to running this code

def checkdatatype():
    print('To check the datatype of each dataset\nActivity table\n')
    print(Activity_table.dtypes)
    print('------------\nBehavioural table')
    print(Behavioural_table.dtypes,'\n------------\nCampaigns table')
    print(Campaigns_table.dtypes)

def normalize_dataset(df):
    K=df.str.lower()
    K=K.str.replace('-','_').str.replace(' ','_').replace('','unknown').replace(np.nan,'unknown').str.replace('_','')
    
    
    
    return K
    
    
    
    

import pandas as pd
import numpy as np

Behavioural_file_name='Behavioural Data.jsonl'
Behavioural_table=pd.read_json(path_or_buf=Behavioural_file_name,lines=True)
Activity_file_name='Activity Data.csv'
Activity_table=pd.read_csv(Activity_file_name)
Campaigns_file_name='Campaigns Data.parquet'
Campaigns_table=pd.read_parquet(Campaigns_file_name,engine='fastparquet') #Need to install pip fastparquet
Activity_table.timestamp=pd.to_datetime(Activity_table.timestamp,format='mixed') # To format the timestamp in Activity_table.timestamp
Behavioural_table.time=pd.to_datetime(Behavioural_table.time.str.replace('T',' '),format='mixed')
#---------Following is to split the dict of meta into columns and merge into Behavioural_table
list_temp1=pd.DataFrame(Behavioural_table['meta'].tolist())
Behavioural_table=Behavioural_table.join(list_temp1)
Behavioural_table=Behavioural_table.drop(columns='meta')
Behavioural_table.duration_seconds=pd.to_numeric(Behavioural_table.duration_seconds,errors='coerce').astype('Int64')





checkdatatype()

print('We found that the person_id and campaign id datatype is not aligned so I decide to change from float to int for produce standard structure')
Behavioural_table=Behavioural_table.convert_dtypes()
Activity_table=Activity_table.convert_dtypes()
Campaigns_table=Campaigns_table.convert_dtypes()

checkdatatype()

#-------------Check whether the category is normalized
print('------------Before normalization-----------')
print(Behavioural_table['type'].unique())
print(Behavioural_table['source'].unique())
print(Activity_table['activity_type'].unique())
print(Activity_table['detail'].unique())
#To normalize category
Behavioural_table['type']=normalize_dataset(Behavioural_table['type'])
Behavioural_table['source']=normalize_dataset(Behavioural_table['source'])
Activity_table['activity_type']=normalize_dataset(Activity_table['activity_type'])
Activity_table['detail']=normalize_dataset(Activity_table['detail'])
#Check all categories are normalized
print('------------After normalization-----------')
print(Behavioural_table['type'].unique())
print(Behavioural_table['source'].unique())
print(Activity_table['activity_type'].unique())
print(Activity_table['detail'].unique())

#Data cleansing completed


