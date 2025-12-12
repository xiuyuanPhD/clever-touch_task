#fastparquet model is needed. If not available, please type in 'pip install fastparquet' prior to running this code

import pandas as pd

Behavioural_file_name='Behavioural Data.jsonl'
Behavioural_table=pd.read_json(path_or_buf=Behavioural_file_name,lines=True)
Activity_file_name='Activity Data.csv'
Activity_table=pd.read_csv(Activity_file_name)
Campaigns_file_name='Campaigns Data.parquet'
Campaigns_table=pd.read_parquet(Campaigns_file_name,engine='fastparquet') #Need to install pip fastparquet

