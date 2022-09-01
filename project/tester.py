from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
import sys
from datetime import timedelta, date
import json
import pandas as pd
import os
import psycopg2

conn = psycopg2.connect(
   database="addinsights", user='pranav', password='Pranav12345', host='127.0.0.1', port= '5432'
)

cursor = conn.cursor()
cursor.execute("TRUNCATE TABLE ad_insights")
conn.commit()

cursor.execute("SELECT (id) FROM ad_insights ORDER BY id DESC")
id_data = cursor.fetchone()
if id_data is None:
    id_data_int = 0
else:
    id_data_int = id_data[0]




#arg1 = sys.argv[1] #start date
#arg2 = sys.argv[2] #end date
#arg3 = sys.argv[3] #account_id
arg1 = '2022-08-08' #sample arguments
arg2 = '2022-08-14'
arg3 = 'act_3445717322189461'

os_username = os.environ.get('USERNAME') #finding enviromental variable 'user' 
my_path = fr"C:/Users/{os_username}/facebook_api_data/"+arg3+"/" 

#set up new directory
try:
    os.makedirs(my_path,exist_ok=True)
except OSError as error : #dodge directory already exists error
    t=1

#function to help iterate between two dates
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)



#turning user inputed dates into date type values
days_in_month = []
d_1 = int(arg1[8:10])
d_2 = int(arg2[8:10])
m_1 = int(arg1[5:7])
m_2 = int(arg2[5:7])
year_1 = int(arg1[0:4])
year_2 = int(arg2[0:4])
#print(d_1)
#print(m_1)

start_date = date(year_1,m_1,d_1)
end_date = date(year_2,m_2,d_2+1)

#setup for API call
app_id = '23849329208400670'
app_secret = 'cb36d0097ead52440d528d1d392f1275'
access_token = 'EAAmJXZBij9tsBAD91tFfTqqB3y8ytKBZCr7B4Cte5b4ZC9BZBr7SpXkW3PZCXKD9njM1q5a0lzIkYaQ3hdY1ZBmBtlFq8VgZCgqbsFOZCxsZBgE2lgPLIKgTOZAzMbO66cZBcJ2zk99HtsA8ZCDaCXtW0kATDgBL6yXtLUHYSMcuMG7eG9mILlvl6hY9'

FacebookAdsApi.init(app_id, app_secret, access_token)


#API calls for each day from start date to end date for each campaign id
for single_date in daterange(start_date, end_date):
    day_d=(single_date.strftime("%Y-%m-%d"))
    #API call to find all campaigns in an account
    params = {
            'level': 'campaign',
            'time_range':{'since': day_d,'until':day_d,
                 
                          },
            #'time_increment': 1,
            #'date_preset': 'last_7d' 
            }

    fields = [
            'campaign_id',
            'campaign_name',


            ]

    insights = AdAccount(arg3).get_insights(
            params = params,
            fields = fields,
            )

    index = 0
    campaign_id_list =[] #empty list for campaign ids
    results = []         #empty list for insights data

    #prepare data for data frame
    for i in insights:
        data = dict(i)
        results.append(data)
    #print(results)
    length = len(results)
    df= pd.DataFrame(results) #insert insight data into a data frame (table)

    #read campaign ids from table and put them into campaign_id_list
    for i in range(length):
        l = df.at[i,'campaign_id']
        if l == '23850273656550670':
            print('match')
        campaign_id_list.append(l)
    print(campaign_id_list)
