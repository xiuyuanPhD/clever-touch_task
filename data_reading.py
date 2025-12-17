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

#To delete duplicate based on activity id
Behavioural_table=Behavioural_table.drop_duplicates(subset='id')
Activity_table=Activity_table.drop_duplicates(subset='activity_id')

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

#To detele all na values
# Activity_table=Activity_table.dropna(subset=['campaign_id','person_id'])
# Behavioural_table=Behavioural_table.dropna(subset=['campaign','person'])

#Decided not to drop rows with nan person_id

Activity_table=Activity_table.dropna(subset=['campaign_id'])
Behavioural_table=Behavioural_table.dropna(subset=['campaign'])

#sort the data by pampaign, person and time
# Behavioural_table=Behavioural_table.sort_values(by=['campaign','person','time'])
# Activity_table=Activity_table.sort_values(by=['campaign_id','person_id','timestamp'])

#Rename behavioural table

Behavioural_table=Behavioural_table.rename(columns={"id":"activity_id","campaign":"campaign_id","person":"person_id","type":"activity_type","time":"timestamp"})
#Delete column duration_seconds in behavioural table

Behavioural_table=Behavioural_table.drop(columns='duration_seconds')

# Behavioural_table=Behavioural_table.sort_values(by=['person_id','campaign_id','timestamp'])
# Activity_table=Activity_table.sort_values(by=['person_id','campaign_id','timestamp'])

#To merge two tables

Final_data=pd.concat([Activity_table,Behavioural_table])

#Sort based on person id
Final_data=Final_data.sort_values(by=['person_id','campaign_id','timestamp'])

#delete rows with unknown activity type
mask=Final_data['activity_type']=='unknown'
Final_data=Final_data[~mask]

#Data cleansing completed
#Merge campaign table into final data
Final_data=Final_data.join(Campaigns_table.set_index('campaign_id'),on='campaign_id')

#Output data into excel
Final_data.to_excel('structured_final_data.xlsx')

