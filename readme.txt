Instructions

1. Please make sure that modules including pandas, fastparquet, numpy and matplotlib are installed. If not, please install modules by running ‘pip install ModuleName’ in console
2. Run ‘data_reading.py’, this will read all datasets, generate standard structured data and write into ‘/output/structured_final_data.xlsx’
3. Run ‘Data_analyse.py’. This will analyse the data and generate the output excel into ‘output/output_result.xlsx’. This will also create bar chart of the statistics of number of activities (output/bar_chart_num_per_campaign.png) and most three types of activities per campaign (output/campaign number.png, in total 15 pictures)


Approach
The original data needs data cleansing process. This includes deleting duplicated data, formatting the datatype (e.g, to format timestamp for all datasets), dataset normalising (for example, there are activity type of web_visit, web-visit and WebVisit, I choose to normalise all the type to webvisit [all lower case] and it will simplifier the process), processing nan data (here I choose only drop the data with unknown campaign_id and unknown activity type because the relationship between activity type and campaign_id is of interest), and dataset merging.