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

dataset=pd.read_excel('output/structured_final_data.xlsx')

#Count number of activities, and most commonly engaged activity type per campaign
max_campaign=max(dataset['campaign_id'])
list_num=[]
campaign_count=[]
most_activity=[]
Second_activity=[]
Third_activity=[]
Most_activity_count=[]
Second_activiey_count=[]
Third_activity_count=[]
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
    Third_activity.append(activity_count.index[2])
    Most_activity_count.append(activity_count.array[0].item())
    Second_activiey_count.append(activity_count.array[1].item())
    Third_activity_count.append(activity_count.array[2].item())
Num_of_activity=pd.DataFrame(data={'Campaign_number':list_num,'Number_of_activities':campaign_count,'Most_activity':most_activity,'Most_activity_count':Most_activity_count,
                                   'Second_activity':Second_activity,'Second_activity_count':Second_activiey_count,'Third_activity':Third_activity,'Third_activity_count':Third_activity_count})


#Number of activiey per owner

num_per_owner=dataset['owner'].value_counts()
#Number of activity per person
num_per_person=dataset['person_id'].value_counts()

#Write result into the excel

with pd.ExcelWriter('output/output_result.xlsx') as writer:
    Num_of_activity.to_excel(writer,sheet_name='num_of_activities')
    num_per_owner.to_excel(writer,sheet_name='num_per_owner')
    num_per_person.to_excel(writer,sheet_name='num_per_person')
print(np.mean(num_per_person))

#output the figure of number per campaign and save into bar_chart_num_per_campaign.png
fig,ax=plt.subplots()


plt.bar(Num_of_activity.Campaign_number.astype('str'),Num_of_activity.Number_of_activities)
plt.xlabel('Campaign number')
plt.ylabel('Number of activities per campaign')
plt.show()
fig.savefig('output/bar_chart_num_per_campaign.png')

#Analyse the event count for each campaign
for i in range(15):
    Campaign_number_idx=i+1
    x_label=Num_of_activity.loc[i,['Most_activity','Second_activity','Third_activity']]
    y_value=Num_of_activity.loc[i,['Most_activity_count','Second_activity_count','Third_activity_count']]
    fig,ax=plt.subplots()
    plt.bar(x_label,y_value)
    plt.xlabel('Activity type')
    plt.ylabel('Number of activities')
    title_label='Campaign '+str(Campaign_number_idx)
    plt.title(title_label)
    filename='output/'+title_label+'.png'
    fig.savefig(filename)
    
    
    
    