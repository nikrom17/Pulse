import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime
import requests

CLIENT_ID = '22CXX5'
CLIENT_SECRET = '7a9dd09c1b62b1c0a262380aeb8c900e'

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])

auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

fit_statsHR = auth2_client.intraday_time_series('activities/heart', base_date='2018-07-24', detail_level='1sec')

time_list = []
val_list = []
for i in fit_statsHR['activities-heart-intraday']['dataset']:
    val_list.append(i['value'])
    time_list.append(i['time'])
heartdf = pd.DataFrame({'Heart Rate':val_list,'Time':time_list})
#print(heartdf)

fit_statsSl = auth2_client.sleep(date='today')
stime_list = []
sval_list = []
for i in fit_statsSl['sleep'][0]['minuteData']:
    stime_list.append(i['dateTime'])
    sval_list.append(i['value'])
sleepdf = pd.DataFrame({'State':sval_list,
                     'Time':stime_list})
sleepdf['Interpreted'] = sleepdf['State'].map({'2':'Awake','3':'Very Awake','1':'Asleep'})
#print(sleepdf)

fit_statsACT = auth2_client.time_series(resource='activities', base_date='2018-07-24', period='1d')
print(fit_statsACT)
