#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 14:19:01 2025

@author: xiuyuanyang
"""

#Load structured data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dataset=pd.read_excel('structured_final_data.xlsx')

#Count number of activities, and most commonly engaged activity type per campaign
max_campaign=max(dataset['campaign_id'])
list_num=[]
campaign_count=[]
most_activity=[]
Second_activity=[]
Third_activity=[]
for campaign_num in range(max_campaign):
    #print(campaign_num+1)
    k=dataset['campaign_id']==campaign_num+1
    l=dataset['campaign_id'][k]
    acitivy_list=dataset['activity_type'][k]
    activity_count=acitivy_list.value_counts()
    max_activity=activity_count.index[0]
    list_num.append(campaign_num+1)
    campaign_count.append(l.size)
    most_activity.append(max_activity)
    Second_activity.append(activity_count.index[1])
    Third_activity.append(activity_count.index[3])
Num_of_activity=pd.DataFrame(data={'Campaign_number':list_num,'Numer_of_activity':campaign_count,'Most_activity':most_activity,'Second_activity':Second_activity,'Third_activity':Third_activity})


#Number of activiey per owner

num_per_owner=dataset['owner'].value_counts()
#Number of activity per person
num_per_person=dataset['person_id'].value_counts()

#Write result into the excel

with pd.ExcelWriter('output_result.xlsx') as writer:
    Num_of_activity.to_excel(writer,sheet_name='num_of_activities')
    num_per_owner.to_excel(writer,sheet_name='num_per_owner')
    num_per_person.to_excel(writer,sheet_name='num_per_person')
print(np.mean(num_per_person))
fig,ax=plt.subplots()
ax.hist(num_per_person,10)

plt.show()